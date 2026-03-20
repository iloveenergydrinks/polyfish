"""
Polymarket market metadata routes.
"""

from flask import jsonify, request

from . import market_bp
from ..models.project import ProjectManager, ProjectStatus
from ..services.ontology_generator import OntologyGenerator
from ..services.polymarket_service import PolymarketService
from ..utils.logger import get_logger

logger = get_logger("polyfish.api.market")


@market_bp.route("/active", methods=["GET"])
def list_active_markets():
    try:
        limit = request.args.get("limit", 24, type=int)
        offset = request.args.get("offset", 0, type=int)

        service = PolymarketService()
        markets = service.list_active_markets(limit=limit, offset=offset)

        return jsonify(
            {
                "success": True,
                "data": {
                    "markets": markets,
                    "limit": limit,
                    "offset": offset,
                    "count": len(markets),
                    "has_more": len(markets) == max(1, min(limit, 100)),
                },
            }
        )
    except Exception as exc:
        logger.error(f"Failed to list active Polymarket markets: {exc}")
        return jsonify({"success": False, "error": str(exc)}), 500


@market_bp.route("/lookup", methods=["GET"])
def lookup_market():
    try:
        market_id = (request.args.get("id", "") or "").strip()
        market_slug = (request.args.get("slug", "") or "").strip()

        if not market_id and not market_slug:
            return jsonify({"success": False, "error": "Please provide a market id or slug"}), 400

        service = PolymarketService()
        market = service.get_market(market_id=market_id or None, slug=market_slug or None)

        return jsonify(
            {
                "success": True,
                "data": {
                    "market": market,
                },
            }
        )
    except Exception as exc:
        logger.error(f"Failed to look up Polymarket market: {exc}")
        return jsonify({"success": False, "error": str(exc)}), 500


@market_bp.route("/project", methods=["POST"])
def create_project_from_market():
    try:
        payload = request.get_json() or {}
        simulation_requirement = (payload.get("simulation_requirement") or "").strip()
        if not simulation_requirement:
            return jsonify({"success": False, "error": "Please provide simulation_requirement"}), 400

        market_slug = payload.get("market_slug")
        market_id = payload.get("market_id")
        provided_market = payload.get("market")

        market_service = PolymarketService()
        if isinstance(provided_market, dict) and provided_market.get("question"):
            market = provided_market
        else:
            market = market_service.get_market(market_id=market_id, slug=market_slug)

        project_name = (payload.get("project_name") or market.get("question") or "PolyFish Market").strip()
        project = ProjectManager.create_project(name=project_name)
        project.simulation_requirement = simulation_requirement

        seed_text = market_service.build_market_seed_text(market)
        ProjectManager.save_extracted_text(project.project_id, seed_text)

        project.files = [
            {
                "filename": f"market:{market.get('slug') or market.get('id')}",
                "size": len(seed_text),
            }
        ]
        project.total_text_length = len(seed_text)

        generator = OntologyGenerator()
        ontology = generator.generate(
            document_texts=[seed_text],
            simulation_requirement=simulation_requirement,
            additional_context=(
                "The source is live Polymarket market metadata only. "
                "Model the market as a forecastable social-information environment."
            ),
        )

        project.ontology = {
            "entity_types": ontology.get("entity_types", []),
            "edge_types": ontology.get("edge_types", []),
        }
        project.analysis_summary = ontology.get("analysis_summary", "")
        project.status = ProjectStatus.ONTOLOGY_GENERATED
        ProjectManager.save_project(project)

        return jsonify(
            {
                "success": True,
                "data": {
                    "project_id": project.project_id,
                    "project_name": project.name,
                    "ontology": project.ontology,
                    "analysis_summary": project.analysis_summary,
                    "files": project.files,
                    "total_text_length": project.total_text_length,
                    "market": market,
                },
            }
        )
    except Exception as exc:
        logger.error(f"Failed to create project from Polymarket market: {exc}")
        return jsonify({"success": False, "error": str(exc)}), 500
