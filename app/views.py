from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from . import db
from .models import BasketItem, Product

views = Blueprint("views", __name__)

CATEGORIES = ("football", "basketball", "running")


def _img_url(filename: str) -> str:
    return url_for("static", filename=f"img/{filename}")


def _products_for_category(category: str):
    products = Product.query.filter_by(category=category).all()
    products_with_urls = [{"product": p, "url": _img_url(p.name)} for p in products]
    return products, products_with_urls


@views.route("/")
def home():
    offers = Product.query.filter_by(is_special_offer=True).all()
    offers_with_urls = [{"product": p, "url": _img_url(p.name)} for p in offers]

    return render_template(
        "index.html",
        user=current_user,
        special_offers=offers_with_urls,
    )


@views.route("/football")
def football():
    products, products_with_urls = _products_for_category("football")
    return render_template(
        "football.html",
        user=current_user,
        products=products,
        products_with_urls=products_with_urls,
    )


@views.route("/basketball")
def basketball():
    products, products_with_urls = _products_for_category("basketball")
    return render_template(
        "basketball.html",
        user=current_user,
        products=products,
        products_with_urls=products_with_urls,
    )


@views.route("/running")
def running():
    products, products_with_urls = _products_for_category("running")
    return render_template(
        "running.html",
        user=current_user,
        products=products,
        products_with_urls=products_with_urls,
    )


@views.route("/basket", methods=["GET"])
@login_required
def basket_page():
    basket_items = BasketItem.query.filter_by(user_id=current_user.id).all()

    total = 0.0
    for item in basket_items:
        total += float(item.product.price) * int(item.quantity)

    return render_template(
        "basket.html", user=current_user, basket_items=basket_items, total=total
    )


@views.route("/basket", methods=["POST"])
@login_required
def basket_add():
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)
    size = (data.get("size") or "").strip()

    if not product_id:
        return jsonify({"error": "product_id is required"}), 400

    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "quantity must be a positive integer"}), 400

    if not size:
        return jsonify({"error": "size is required"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    basket_item = BasketItem.query.filter_by(
        user_id=current_user.id, product_id=product_id, size=size
    ).first()

    if basket_item:
        basket_item.quantity += quantity
    else:
        basket_item = BasketItem(
            user_id=current_user.id, product_id=product_id, quantity=quantity, size=size
        )
        db.session.add(basket_item)

    db.session.commit()
    return jsonify({"message": "Added to basket"}), 200


@views.route("/product_management", methods=["GET", "POST"])
@login_required
def product_management():
    if request.method == "POST":
        if request.form.get("product_id_to_remove"):
            return _handle_remove_product()

        # If we have any of the add-product fields, treat it as an add attempt
        if request.form.get("product_name") or request.files.get("pic"):
            return _handle_add_product()

    products = Product.query.all()
    return render_template(
        "product_management.html", user=current_user, products=products
    )


def _handle_remove_product():
    product_id = request.form.get("product_id_to_remove")
    product = Product.query.get(product_id)

    if not product:
        flash("Product not found!", category="error")
        return redirect(url_for("views.product_management"))

    filename = product.name  # keep before delete
    db.session.delete(product)
    db.session.commit()

    img_path = Path(current_app.root_path) / "static" / "img" / filename
    try:
        img_path.unlink(missing_ok=True)  # safe delete if file exists
    except Exception:
        # Not fatal: product is already removed from DB
        pass

    flash("Product deleted!", category="success")
    return redirect(url_for("views.product_management"))


def _handle_add_product():
    product_name = (request.form.get("product_name") or "").strip()
    category = (request.form.get("category") or "").strip()
    price = request.form.get("price")
    quantity = request.form.get("quantity")
    sizes = (request.form.get("sizes") or "").strip()
    pic = request.files.get("pic")
    is_special_offer = request.form.get("is_special_offer") == "on"

    if not pic or not pic.filename:
        flash("Please upload a product image.", category="error")
        return redirect(url_for("views.product_management"))

    if not product_name:
        flash("Product name is required.", category="error")
        return redirect(url_for("views.product_management"))

    if category not in CATEGORIES:
        flash("Invalid category.", category="error")
        return redirect(url_for("views.product_management"))

    try:
        price_value = float(price)
        if price_value < 0:
            raise ValueError
    except (TypeError, ValueError):
        flash("Price must be a valid non-negative number.", category="error")
        return redirect(url_for("views.product_management"))

    try:
        quantity_value = int(quantity)
        if quantity_value < 0:
            raise ValueError
    except (TypeError, ValueError):
        flash("Quantity must be a valid non-negative integer.", category="error")
        return redirect(url_for("views.product_management"))

    if not sizes:
        flash("Sizes are required (e.g., 'S,M,L' or '8,9,10').", category="error")
        return redirect(url_for("views.product_management"))

    filename = secure_filename(pic.filename)

    img_folder = Path(current_app.root_path) / "static" / "img"
    img_folder.mkdir(parents=True, exist_ok=True)

    save_path = img_folder / filename
    pic.save(save_path)

    new_product = Product(
        product_name=product_name,
        name=filename,
        category=category,
        price=price_value,
        quantity=quantity_value,
        sizes=sizes,
        is_special_offer=is_special_offer,
    )
    db.session.add(new_product)
    db.session.commit()

    flash("Product added!", category="success")
    return redirect(url_for("views.product_management"))
