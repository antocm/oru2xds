#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Antonio Martins (digiplan.pt@gmail.com)
#

# Adapted from BASH version in https://maarten.mulders.it/2018/12/troubleshooting-soap-and-mtom-using-the-command-line/

import uuid
import requests
import logging
import os
import re
from urllib3.filepost import encode_multipart_formdata, choose_boundary
from urllib3.fields import RequestField

###################################################################
## Global variables
###################################################################


logger = logging.getLogger('oru2xds')


###################################################################
## Functions
###################################################################


def encode_multipart_related(fields, boundary = None):
	if boundary is None:
		boundary = choose_boundary()
	body, _ = encode_multipart_formdata(fields, boundary)
	content_type = str('multipart/related; boundary=%s' % boundary)
	return body, content_type


def encode_media_related(xds_request_id, xds_request, attchment_id, attachment):
	rf1 = RequestField(
		name = 'xds_request',
		data = xds_request,
		headers = {'Content-Type': 'application/xop+xml; charset=UTF-8; type="application/soap+xml"',
				'Content-Transfer-Encoding': 'binary',
				'Content-ID': xds_request_id
		},
	)
	rf2 = RequestField(
		name = 'attachment1',
		data = attachment,
		headers = {'Content-Type': 'text/plain',
			'Content-Transfer-Encoding': 'binary',
			'Content-ID': attchment_id
		},
	)
	return encode_multipart_related([rf1, rf2])


def send_soap(service_URL, REQUEST_BODY, REQUEST_ID, ATTACHMENT_BODY, ATTACHMENT_ID):

	soap_action = "urn:ihe:iti:2007:ProvideAndRegisterDocumentSet-b"

	logger.info('Calling requests to perform the SOAP service')

	session = requests.Session()
	body, content_type = encode_media_related(
		REQUEST_ID,
		REQUEST_BODY,
		ATTACHMENT_ID,
		ATTACHMENT_BODY
	)

	headers = {
		'user-agent': 'oru2xds/1.0.0',
		'Content-Type': content_type + '; type="application/xop+xml"; start="{}"; start-info="application/soap+xml"; action="{}"'.format(REQUEST_ID, soap_action)
	}

	server_response = session.post(service_URL, data = body, headers = headers)
	# s = requests.Session()
	# req = requests.Request("POST", service_URL, headers = headers, files = files)
	# prepped = req.prepare()
	# NOT WORKING del prepped.headers['Accept-Encoding']
	# print(prepped.headers)
	# resp = s.send(prepped)
	exit()

	try:
		server_response = requests.post(service_URL, headers = headers, files = files)
		server_response.raise_for_status()
	except requests.exceptions.RequestException as err:
		logger.exception("Error: {}".format(err))
		return None
	except requests.exceptions.HTTPError as errh:
		logger.exception("HTTP Error: {}".format(errh))
		return None
	except requests.exceptions.ConnectionError as errc:
		logger.exception("Error Connecting: {}".format(errc))
		return None
	except requests.exceptions.Timeout as errt:
		logger.exception("Timeout Error: {}".format(errt))
		return None

	if server_response.status_code == requests.codes.ok:
		logger.info("SOAP service called successfully")
	else:
		logger.excetpion("SOAP service FAILED. Return code was: {}{}{}".format(server_response.status_code, os.linesep, server_response.raise_for_status()))
		return None

	logger.info('SOAP service finished')
	logger.info('Server response here: {}{}'.format(os.linesep, server_response.text))

	# print(server_response.text)
	# res1 = re.sub(r'Content.*\n', '', server_response.text)
	# res1 = re.sub(r'--.*\n', '', res1)
	# res1 = re.sub(r'^\n', '', res1)
	# print(res1)
	return server_response.text
	# return res1


if __name__ == "__main__":
	# For debugging purposes
	service_URL = "http://localhost:8080/tf6/services/xdsrepositoryb"
	ATTACHMENT_BODY='''<?xml version='1.0' encoding='UTF-8'?>
<?xml-stylesheet type="text/xsl" href="https://registry.xds.srsa.local:8085/hh-cda-stylesheet/cda_hh.xsl"?>
<ClinicalDocument xmlns="urn:hl7-org:v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:hl7-org:v3 CDA.xsd">
  <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
  <templateId root="2.16.840.1.113883.10.20.6"/>
  <id extension="a6mb8-38912-mfl94-12509" root="2.16.840.1.113883.2.10.1.2.1"/>
  <code code="18748-4" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Diagnostic Imaging Report"/>
  <title>Diagnostic Imaging Report</title>
  <effectiveTime value="20201007142209"/>
  <confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25"/>
  <languageCode code="pt-PT"/>
  <component>
    <structuredBody>
      <component>
        <section>
          <templateId root="2.16.840.1.113883.10.20.6.1.2"/>
          <code code="18782-3" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Findings"/>
          <title>Observação</title>
          <text>TEST1</text>
        </section>
      </component>
    </structuredBody>
  </component>
</ClinicalDocument>
'''
	REQUEST_BODY='''<?xml version='1.0' encoding='UTF-8'?>
<Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope" xmlns:wsa="http://www.w3.org/2005/08/addressing">
  <soapenv:Header>
    <wsa:To>http://localhost:8080/tf6/services/xdsrepositoryb</wsa:To>
    <wsa:MessageID mustUnderstand="true">urn:uuid:99d724de-6590-11eb-b507-39c60dd988ef</wsa:MessageID>
    <wsa:Action>urn:ihe:iti:2007:ProvideAndRegisterDocumentSet-b</wsa:Action>
  </soapenv:Header>
  <soapenv:Body>
    <ProvideAndRegisterDocumentSetRequest xmlns:xdsb="urn:ihe:iti:xds-b:2007">
      <SubmitObjectsRequest xmlns:lcm="urn:oasis:names:tc:ebxml-regrep:xsd:lcm:3.0">
        <RegistryObjectList>
        </RegistryObjectList>
      </SubmitObjectsRequest>
      <Document id="Document01">
        <Include xmlns:xop="http://www.w3.org/2004/08/xop/include" href="cid:1.urn:uuid:99d724dd-6590-11eb-b507-39c60dd988ef@oru2xds"/>
      </Document>
    </ProvideAndRegisterDocumentSetRequest>
  </soapenv:Body>
</Envelope>
'''
	REQUEST_ID = "<0.urn:uuid:{}@oru2xds>".format(str(uuid.uuid1()))
	ATTACHMENT_ID = "<1.urn:uuid:{}@oru2xds>".format(str(uuid.uuid1()))
	send_soap(service_URL, REQUEST_BODY, REQUEST_ID, ATTACHMENT_BODY, ATTACHMENT_ID)

