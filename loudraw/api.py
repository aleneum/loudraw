from flask import Flask
from flask_restful import Resource, Api, fields, reqparse

import threading

_flask_scaper = None
_flask_server = None
_flask_thread = None

CREATE_UNDIRECTED_FIELDS = {
    'cx': (float, 0.0),
    'cy': (float, 0.0),
    'radius': (float, 0.2),
    'blurx': (float, 0.1),
    'blury': (float, 0.1),
    'source': (str, "/Users/amilab/forrest.wav"),
    'angle': (int, 10),
    'loop': (bool, True)
}

EDIT_FIELDS = {
    'cx': (float, None),
    'cy': (float, None),
    'radius': (float, None),
    'blurx': (float, None),
    'blury': (float, None),
    'angle': (int, None),
    'rotation': (int, None)
}

PARSER_CREATE_UNDIRECTED = reqparse.RequestParser()
PARSER_EDIT = reqparse.RequestParser()

for p, t in CREATE_UNDIRECTED_FIELDS.items():
    PARSER_CREATE_UNDIRECTED.add_argument(p,  type=t[0], default=t[1], required=False)

for p, t in EDIT_FIELDS.items():
    PARSER_EDIT.add_argument(p,  type=t[0], default=t[1], required=False)


class UndirectedFactory(Resource):

    def get(self):
        args = PARSER_CREATE_UNDIRECTED.parse_args()
        i = _flask_scaper.add_object('undirected', center=(args.cx, args.cy),
                                     radius=args.radius, blur=(args.blurx, args.blury))
        _flask_server.init_mixer(i, file_path=args.source, loop=True,
                                 channels=_flask_scaper.amp_from_image(_flask_scaper.objects[i].canvas))
        return i


class DirectedFactory(Resource):

    def get(self):
        args = PARSER_CREATE_UNDIRECTED.parse_args()
        i = _flask_scaper.add_object('directed', center=(args.cx, args.cy),
                                     radius=args.radius, angle=args.angle)
        _flask_server.init_mixer(i, file_path=args.source, loop=True,
                                 channels=_flask_scaper.amp_from_image(_flask_scaper.objects[i].canvas))
        return i


class ObjectEditor(Resource):

    def get(self, object_id):
        args = PARSER_EDIT.parse_args()
        o = _flask_scaper.objects[object_id]
        if args['cx'] is not None and args['cy'] is not None:
            o.center = (args.cx, args.cy)

        if args['radius'] is not None:
            o.radius = args.radius

        if args['blurx'] is not None and args['blury'] is not None:
            o.blur = (args.blurx, args.blury)
        if args['angle'] is not None:
            o.angle = args.angle
        if args['rotation'] is not None:
            o.rotation = args.rotation
        o.draw()
        _flask_server.set_mixer(object_id, _flask_scaper.amp_from_image(o.canvas))


def start_app(scaper, server, threaded=True, host=None):
    global _flask_scaper, _flask_server, _flask_thread
    _flask_scaper = scaper
    _flask_server = server
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(UndirectedFactory, '/create/undirected')
    api.add_resource(DirectedFactory, '/create/directed')
    api.add_resource(ObjectEditor, '/set/<int:object_id>')

    if threaded:
        _flask_thread = threading.Thread(target=app.run, kwargs=dict(debug=True, use_reloader=False, host=host))
        _flask_thread.start()
    else:
        app.run(debug=True, host=host)
