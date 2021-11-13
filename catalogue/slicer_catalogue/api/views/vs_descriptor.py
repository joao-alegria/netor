from flask import Blueprint, request
from marshmallow import ValidationError
from http import HTTPStatus
from api.exceptions.utils import handle_exception
from api.serializers.vs_descriptor import VsDescriptorSerializer
from api.views.utils import response_template
from api.exceptions.exceptions import BadVsBlueprintBody
from api.auth import login_required, current_user
import api.queries.vs_descriptor as queries

app = Blueprint('vsdescriptor', __name__)

handle_exception(app)  # Handle errors


@app.route("/vsdescriptor", methods=('GET',))
@login_required
def get_vs_descriptors():
    args = {
        'tenant_id': current_user.name,
        'vsd_id': request.args.get('vsd_id'),
        'is_admin': current_user.is_admin()
    }

    serializer = VsDescriptorSerializer(many=True)
    data = serializer.dump(queries.get_vs_descriptors(**args))

    return response_template('Success', data)


@app.route('/vsdescriptor', methods=('DELETE',))
@login_required
def delete_vs_descriptor():
    args = {
        'tenant_id': current_user.name,
        'vsd_id': request.args.get('vsd_id'),
        'is_admin': current_user.is_admin()
    }

    queries.delete_vs_descriptor(**args)
    return response_template('Success', status_code=HTTPStatus.NO_CONTENT)


@app.route('/vsdescriptor', methods=('POST',))
@login_required
def create_vs_descriptor():
    request_data = request.get_json()

    serializer = VsDescriptorSerializer()
    try:
        validated_data = serializer.load(request_data)
    except ValidationError as error:
        raise BadVsBlueprintBody(error.messages)

    vs_descriptor_id = queries.create_vs_descriptor(validated_data)
    return response_template('Success', data={'vs_descriptor_id': vs_descriptor_id}, status_code=HTTPStatus.CREATED)
