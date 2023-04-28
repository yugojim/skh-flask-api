import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import xmltodict
import Function

#fhir = 'http://104.208.68.39:8080/fhir/'#4600VM
#fhir = "http://61.67.8.220:8080/fhir/"#skh outside
fhir = "http://10.2.1.17:8080/fhir/"#skh inside
#fhir = "http://106.105.181.72:8080/fhir/"#tpech

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

###serverstatus###
@app.route('/', methods=['GET'])
@cross_origin()
def serverstatus():
    return jsonify({'Server Status' : 'run'}), 200

###DischargeSummary###
@app.route('/DischargeSummary/<string:DischargeSummary_Id>', methods=['GET'])
@cross_origin()
def query_DischargeSummary(DischargeSummary_Id):
    url = fhir + 'Composition/' + DischargeSummary_Id
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

@app.route('/DischargeSummary/<string:DischargeSummary_Id>', methods=['POST'])
@cross_origin()
def create_DischargeSummary(DischargeSummary_Id):
    #record = json.loads(request.data)
    #record = json.loads(request.data, strict=False)
    record = xmltodict.parse(request.data)
    Composition, status_code = Function.PostFhirComposition(record, DischargeSummary_Id)
    return jsonify(Composition), status_code

@app.route('/DischargeSummary/<string:DischargeSummary_Id>', methods=['PUT'])
@cross_origin()
def update_DischargeSummary(DischargeSummary_Id):
    record = xmltodict.parse(request.data)
    Composition, status_code = Function.PostFhirComposition(record, DischargeSummary_Id)
    return jsonify(Composition), status_code    
    
@app.route('/DischargeSummary/<string:DischargeSummary_Id>', methods=['DELETE'])
@cross_origin()
def delte_DischargeSummary(DischargeSummary_Id):
    url = fhir + 'Composition/' + DischargeSummary_Id
    payload = {}
    headers = {}
    response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

###VisitNote###
@app.route('/VisitNote/<string:VisitNote_Id>', methods=['GET'])
@cross_origin()
def query_VisitNote(VisitNote_Id):
    url = fhir + 'Composition/' + VisitNote_Id
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

@app.route('/VisitNote/<string:VisitNote_Id>', methods=['POST'])
@cross_origin()
def create_VisitNote(VisitNote_Id):
    record = xmltodict.parse(request.data)
    Composition, status_code = Function.PostFhirComposition(record, VisitNote_Id)
    return jsonify(Composition), status_code

@app.route('/VisitNote/<string:VisitNote_Id>', methods=['PUT'])
@cross_origin()
def update_VisitNote(VisitNote_Id):
    record = xmltodict.parse(request.data)
    Composition, status_code = Function.PostFhirComposition(record, VisitNote_Id)
    return jsonify(Composition), status_code    
    
@app.route('/VisitNote/<string:VisitNote_Id>', methods=['DELETE'])
@cross_origin()
def delte_VisitNote(VisitNote_Id):
    url = fhir + 'Composition/' + VisitNote_Id
    payload = {}
    headers = {}
    response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

###BloodExamination###
@app.route('/BloodExamination/<string:BloodExamination_Id>', methods=['GET'])
@cross_origin()
def query_BloodExamination(BloodExamination_Id):
    url = fhir + 'Composition/' + BloodExamination_Id
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

@app.route('/BloodExamination/<string:BloodExamination_Id>', methods=['POST'])
@cross_origin()
def create_BloodExamination(BloodExamination_Id):
    record = xmltodict.parse(request.data)
    Composition, status_code = Function.PostFhirComposition(record, BloodExamination_Id)
    return jsonify(Composition), status_code

@app.route('/BloodExamination/<string:BloodExamination_Id>', methods=['PUT'])
@cross_origin()
def update_BloodExamination(BloodExamination_Id):
    record = xmltodict.parse(request.data)
    Composition, status_code = Function.PostFhirComposition(record, BloodExamination_Id)
    return jsonify(Composition), status_code    
    
@app.route('/BloodExamination/<string:BloodExamination_Id>', methods=['DELETE'])
@cross_origin()
def delte_BloodExamination(BloodExamination_Id):
    url = fhir + 'Composition/' + BloodExamination_Id
    payload = {}
    headers = {}
    response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=8181, debug=False)
	app.run(host="0.0.0.0", port=8181, debug=True)