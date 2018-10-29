from flask import Flask, jsonify, request
from collections import namedtuple, defaultdict

app = Flask(__name__)

Producto = namedtuple('Producto', ['codigo', 'nombre', 'tipo', 'stock'])
productos = [ Producto(1, 'resma carta', 'papel', 200),
              Producto(2, 'resma oficio', 'papel', 20),
              Producto(3, 'clip metálico', 'articulo-escritorio', 1000),
              Producto(4, 'lápiz azul', 'lápiz', 20),
              Producto(5, 'lápiz negro', 'lápiz', 200),
              Producto(6, 'lápiz rojo', 'lápiz', 121),
              Producto(7, 'lápiz verde', 'lápiz', 57),
              Producto(8, 'lápiz violeta', 'lápiz', 23),
              Producto(9, 'lápiz naranja', 'lápiz', 1000),
              Producto(10, 'corrector lápiz', 'articulo-escritorio', 12),
              Producto(11, 'corrector frasco', 'articulo-escritorio', 101),
              Producto(12, 'plumón pizarra negro', 'plumón', 1),
              Producto(13, 'plumón pizarra azul', 'plumón', 12),
              Producto(14, 'plumón pizarra rojo', 'plumón', 0),
              Producto(15, 'plumón pizarra púrpura', 'plumón', 56),
              Producto(16, 'plumón pizarra verde', 'plumón', 0),
]


def productoToJSON(producto):
    return jsonify(codigo=producto.codigo,
                   nombre=producto.nombre,
                   tipo=producto.tipo,
                   stock=producto.stock)

@app.route('/stock/<int:codigo>')
def mostrarProducto(codigo):
    producto = productos[codigo - 1]
    return productoToJSON(producto)

@app.route('/productos')
def mostrarProductos():
    return jsonify(productos=productos)

carros = defaultdict(list)

@app.route('/compras/agregar', methods=['POST'])
def agregarCarro():
    if request.method == 'POST':
        carros[request.form['id']].append(request.form['codigo'])

@app.route('/compras/comprar', methods=['POST'])
def comprar():
    for p in carro[request.form['id']]:
        print(p.nombre + " comprado!")

