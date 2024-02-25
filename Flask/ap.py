from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Ruchi/Desktop/Sql/ecommerce.db'
db = SQLAlchemy(app)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image_url = db.Column(db.String(255))

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)

# API Endpoints
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image_url': product.image_url
    } for product in products])

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image_url': product.image_url
    })

@app.route('/cart', methods=['GET'])
def get_cart():
    cart_items = CartItem.query.all()
    return jsonify([{
        'id': cart_item.id,
        'product_id': cart_item.product_id,
        'quantity': cart_item.quantity
    } for cart_item in cart_items])

@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    cart_item = CartItem(product_id=product_id, quantity=quantity)
    db.session.add(cart_item)
    db.session.commit()
    return jsonify({'message': 'Product added to cart successfully'})

@app.route('/cart/<int:id>', methods=['DELETE'])
def remove_from_cart(id):
    cart_item = CartItem.query.get_or_404(id)
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Product removed from cart successfully'})

# Database Integration
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
