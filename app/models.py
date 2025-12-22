from flask_login import UserMixin

from . import db


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)

    # NOTE: Keeping both fields to stay compatible with your existing app/DB.
    # Consider merging later (e.g., use product_name only).
    name = db.Column(db.String(100), nullable=False)         # image filename in your app
    product_name = db.Column(db.String(100), nullable=False) # display name

    category = db.Column(db.String(100), nullable=False, index=True)

    price = db.Column(db.Float, nullable=False)
    sizes = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    user = db.relationship("User", back_populates="products")
    is_special_offer = db.Column(db.Boolean, nullable=False, default=False, index=True)


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)

    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    products = db.relationship(
        "Product",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )

    basket_items = db.relationship(
        "BasketItem",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )


class BasketItem(db.Model):
    __tablename__ = "basket_item"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)

    quantity = db.Column(db.Integer, nullable=False, default=1)
    size = db.Column(db.String(50), nullable=False)

    product = db.relationship("Product", backref=db.backref("basket_items", lazy="select"))
    user = db.relationship("User", back_populates="basket_items")

    __table_args__ = (
    db.UniqueConstraint("user_id", "product_id", "size", name="uq_basket_user_product_size"),
)

