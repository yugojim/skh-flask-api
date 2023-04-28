import json
from datetime import datetime
import pathlib
import requests

#fhir = 'http://104.208.68.39:8080/fhir/'#4600VM
#fhir = "http://61.67.8.220:8080/fhir/"#skh outside
fhir = "http://10.2.1.17:8080/fhir/"#skh inside
#fhir = "http://106.105.181.72:8080/fhir/"#tpech

def component2section(component_dict):
    section = {
        'title': '',
        'code': {'coding': []},
        'text': {},
        'entry': []
        }
   
    try:
        coding = {
            "system": component_dict['section']['code']['@codeSystem'],
            "code": component_dict['section']['code']['@code'],
            "display": component_dict['section']['code']['@displayName']
            }
        section['code']['coding'].append(coding)
        section['title'] = component_dict['section']['title']
        try:
            if component_dict['section']['title'] == '檢驗':
                paragraphText=''
                for p in  component_dict['section']['text']['paragraph']:
                    paragraphText = paragraphText + p + '\n'
                section['text'] =  {'status' : 'additional',\
                                    'div' : '<div xmlns=\"http://www.w3.org/1999/xhtml\">' + paragraphText + '</div>'
                        } 
            else:    
                paragraphText=''
                for p in  component_dict['section']['text']['paragraph']:
                    paragraphText = paragraphText + p
                section['text'] =  {'status' : 'additional',\
                                    'div' : '<div xmlns=\"http://www.w3.org/1999/xhtml\">' + paragraphText + '</div>'
                        } 
        except:
            section['text'] = {'status' : 'additional','div' : '<div xmlns=\"http://www.w3.org/1999/xhtml\"></div>'}

        try:
            if type(component_dict['section']['entry']['observation'])==list:
                for observation in component_dict['section']['entry']['observation']:
                    #print(observation)
                    section['entry'].append({'reference': '','display' : observation['code']['@displayName']})
            else:
                #print(component_dict['section']['entry']['observation']['code'])
                section['entry'].append({'reference': '','display' : component_dict['section']['entry']['observation']['code']['@displayName']})                    
        except:
            None
        
        try:
            #print(type(component_dict['section']['entry']['observationMedia']))
            #print(len(component_dict['section']['entry']['observationMedia']))
            if type(component_dict['section']['entry']['observationMedia'])==list:
                for observationMedia in component_dict['section']['entry']['observationMedia']:
                    #print(observationMedia)
                    section['entry'].append({'reference': '','display' : observationMedia['value']['#text']})
            else:
                #print(component_dict['section']['entry']['observationMedia']['value'])
                section['entry'].append({'reference': '','display' : component_dict['section']['entry']['observationMedia']['value']['#text']})
        except:
            None
        return (section)
    except:
        #print('except')
        return None

def PostFhirComposition(record, DischargeSummary_Id):
    try:
        CompositionjsonPath=str(pathlib.Path().absolute()) + "/Composition_DischargeSummary135726.json"
        Compositionjson = json.load(open(CompositionjsonPath,encoding="utf-8"), strict=False)
        #print(record)
        
        Postxml = record['cdp:ContentPackage']['cdp:ContentContainer']['cdp:StructuredContent']['ClinicalDocument']
        
        Compositionjson['id'] = DischargeSummary_Id
        Compositionjson['resourceType'] = 'Composition'
        Compositionjson['language'] = Postxml['languageCode']['@code']
        Compositionjson['text']['status'] = 'generated'
        
        text = '<table border="1"><caption>出院病摘單</caption><tr><th>身分證字號</th><th>病歷號</th><th>病人姓名</th><th>性別</th><th>出生日期</th><th>文件列印日期</th><th>醫師姓名</th><th>醫師記錄日期時間</th><th>醫院名稱</th><th>住院日期</th><th>出院日期</th><th>轉出醫事機構名稱</th><th>轉入醫事機構名稱</th></tr>'
        text = text + '<tr><td>' + Postxml['recordTarget']['patientRole']['patient']['id']['@extension'] + '</td><td>' + Postxml['recordTarget']['patientRole']['id']['@extension'] + '</td><td>' + Postxml['recordTarget']['patientRole']['patient']['name'] + '</td><td>' + Postxml['recordTarget']['patientRole']['patient']['administrativeGenderCode']['@code'] + '</td><td>' + Postxml['recordTarget']['patientRole']['patient']['birthTime']['@value'] + '</td><td>' + Postxml['effectiveTime']['@value'] + '</td><td>' + Postxml['author']['assignedAuthor']['assignedPerson']['name'] + '</td><td>' + Postxml['author']['time']['@value'] + '</td><td>' + Postxml['recordTarget']['patientRole']['providerOrganization']['name'] + '</td><td>'\
            + Postxml['componentOf']['encompassingEncounter']['effectiveTime']['low']['@value'] + '</td><td>' + Postxml['componentOf']['encompassingEncounter']['effectiveTime']['high']['@value'] + '</td><td>' + Postxml['participant'][1]['associatedEntity']['id']['@extension'] + '</td><td>' + Postxml['participant'][0]['associatedEntity']['id']['@extension'] + '</td></tr></table>'
        
        Compositionjson['text']['div'] = '<div xmlns=\"http://www.w3.org/1999/xhtml\">' + text + '</div>'         
        Compositionjson['status'] = 'preliminary'
        Compositionjson['type'] = {"coding":[{"system":"http://loinc.org","code":"18842-5","display":"Discharge Summary"}]}
        
        datetime_object = datetime.strptime(Postxml['effectiveTime']['@value'], '%Y%m%d%H%M%S')
        Compositionjson['date']=datetime_object.strftime("%Y-%m-%dT%H:%M:%S")
        
        ##Compositionjson['subject']['reference'] = 'Patient/' + Postjson[0]['PAT_NO']
        Compositionjson['subject']['display'] = Postxml['recordTarget']['patientRole']['patient']['name']
        
        Compositionjson['encounter']['display'] = Postxml['componentOf']['encompassingEncounter']['location']
        
        ##Compositionjson['author'][0]['reference'] = 'Practitioner/' + PractitionerPut(xmldict['author']['assignedAuthor'])
        Compositionjson['author'][0]['display'] = Postxml['author']['assignedAuthor']['assignedPerson']['name']
        
        Compositionjson['title'] = Postxml['title']
        Compositionjson['confidentiality'] = 'N'
        Compositionjson['attester'][0]['mode'] = 'professional'
        date_object = datetime.strptime(Postxml['author']['time']['@value'], '%Y%m%d%H%M%S')
        Compositionjson['attester'][0]['time'] = date_object.strftime("%Y-%m-%dT%H:%M:%S")
        
        ##Compositionjson['custodian']['reference'] = 'Organization/' + Postjson[0]['Hospital_Id']
        Compositionjson['custodian']['display'] = Postxml['recordTarget']['patientRole']['providerOrganization']['name']
        
        #for i in range(len(xmldict['component']['structuredBody']['component'])):
        #    Compositionjson['section'].append(component2section(xmldict['component']['structuredBody']['component'][i]))
        component_list = Postxml['component']['structuredBody']['component']
        for i in range(len(component_list)):
            Compositionjson['section'].append(component2section(component_list[i]))
        url = fhir + 'Composition/'+ DischargeSummary_Id
        headers = {
          'Content-Type': 'application/json'
        }
        #print(Compositionjson)
        payload = json.dumps(Compositionjson)
        #print(payload)
        #print(url)
        
        response = requests.request("PUT", url, headers=headers, data=payload)
        #print(response.text)
        resultjson=json.loads(response.text)
        #return (Compositionjson, 201)
        return (resultjson, response.status_code)
    
    except:
        return ({'NG'})