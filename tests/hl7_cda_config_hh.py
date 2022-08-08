###################################################################
## Main configuration
###################################################################


	# This function fills all CDA sections with fixed data order
	# otherwise information taken from the received HL7 message.
	#
	# Use the value hl7message['MSH.F10'] for instances
	# if you want to use the field MSH-10 into a variable that represents
	# some CDA metadata.
	#
	# format hl7message[SEGMENT.Fx.Ry.Cw.Sz] 	for single values
	#
	# If you want a string with multiple fiels, use:
	# hl7message.unescape(str(hl7message.segment('PID')[3][1])))
	# In both cases, the unescaped version of the string will be used.
	# Otherwise fill with fixed strings, or some python function.
	def fill_cda_metadata(self, hl7message):
		logger.info('Assigning HL7 message values into variables')

		# ClinicalDocument/id
		self.m_id = {
			"extension": hl7message['MSH.F10'],
			"id_root": "1.3.6.1.4.1.55196.1.1.2.5"
		}

		# ClinicalDocument/code
		# CONF-DIR-17: The value for ClinicalDocument/code SHOULD be selected from
		# Table 4: LOINC® Document Type Codes 2.16.840.1.113883.6.1 LOINC DYNAMIC
		# and SHOULD be 18748-4 "Diagnostic Imaging Report" 2.16.840.1.113883.6.1 LOINC STATIC .
		# CONF-DIR-18: Implementations MAY use local codes in translation elements to
		# further refine the document type.
		# Consider OBR-4.1 for the exam code
		self.m_code = {
			"code": "18748-4",
			"codeSystem": "2.16.840.1.113883.6.1",
			"codeSystemName": "LOINC",
			"displayName": "Diagnostic Imaging Report",
		}

		# ClinicalDocument/title
		# self.m_title = "Imaging report"
		self.m_title = "Relatório de Imagiologia"

		# ClinicalDocument/effectiveTime
		self.m_effectiveTime = hl7message['OBR.F22']

		# ClinicalDocument/confidentialityCode
		self.m_confidentialityCode = {
			"code": "N",
			"codeSystem": "2.16.840.1.113883.5.25"
		}

		# ClinicalDocument/languageCode
		# self.m_languageCode = "en-US"
		self.m_languageCode = "pt-PT"

		# ClinicalDocument/setId
		self.m_setId = {
			"extension": None,
			"root": None
		}

		# ClinicalDocument/versionNumber
		self.m_versionNumber_value = None
		# self.m_versionNumber_value = "1"

		# This call finds the PID-3 repetition that has the patient ID in the 
		# XDS affinity domain
		# Use this variable instead of "repetition" in the HL7 message
		xad_pid_repetition = hl7_v2x_receiver.Hl7v2x.hl7_find_xad_pid_repetition(hl7message)
		logger.info("Domain assigning authority OID (XAD PID) is present as repetition %s of PID segment", xad_pid_repetition)

		# recordTarget (Patient)
		self.m_patient = {
			"id": hl7message.unescape(str(hl7message.segment('PID')(3)(xad_pid_repetition)(1))),
			"assigningAuthorityName": hl7message.unescape(str(hl7message.segment('PID')(3)(xad_pid_repetition)(4)(1))),
			"assigningAuthorityOID": hl7message.unescape(str(hl7message.segment('PID')(3)(xad_pid_repetition)(4)(2))),
			"name": hl7message.unescape(str(hl7message.segment('PID')(5)(0))),
			"birthdate": hl7message['PID.F7'],
			"sex": hl7message['PID.F8']
		}

		# author
		self.m_author = {
			"time": hl7message['OBR.F22'],
			"id_extension": hl7message['OBR.F32.R1.C1.S1'],
			"id_root": "1.3.6.1.4.1.55196.1.3.2.4",
			"assignedAuthorAssignedPersonName": hl7message['OBR.F32.R1.C1.S2'],
			"assignedAuthorRepresentedOrganizationIdRoot": "1.3.6.1.4.1.55196.1.3",
			"assignedAuthorRepresentedOrganizationName": "Hospital da Horta - Departamento de Radiologia"
		}

		# dataEnterer
		# TODO: To implement

		# informant
		# TODO: To implement

		# custodian
		# Consider representedOrganization_id to be PV1-39
		self.m_custodian = {
			"assignedCustodianRepresentedCustodianOrganizationIdRoot": "1.3.6.1.4.1.55196.1.3",
			"assignedCustodianRepresentedCustodianOrganizationName": "Hospital da Horta - Departamento de Radiologia"
		}

		# informationRecipient
		# TODO: To implement

		# legalAuthenticator
		self.m_legalAuthenticator = {
			"time": hl7message['OBR.F22'],
			"signatureCode": "S",
			"assignedEntityIdExtension": hl7message['OBR.F32.R1.C1.S1'],
			"assignedEntityIdRoot": "1.3.6.1.4.1.55196.1.3.2.4",
			"assignedEntityAssignedPersonName": hl7message['OBR.F32.R1.C1.S2']
		}

		# authenticator
		# TODO: To implement
		# self.m_authenticator = {
		# 	"time": "20060922",
		# 	"signatureCode": "S",
		# 	"assignedEntityIdExtension": "69",
		# 	"assignedEntityIdRoot": "2.16.840.1.113883.2.10.1.1.2",
		# 	"assignedEntityAssignedPersonName": "Ducrey^Gabriel"
		# }

		# participant
		# TODO: To implement

		# inFullfillmentOf
		# CONF-DIR-49: One or more inFullfillmentOf elements MAY be present. They
		# represent the Placer Order that was fulfilled by the imaging procedure(s) covered by
		# this report document.
		self.m_inFullfillmentOf = {
			"id_root": "1.3.6.1.4.1.55196.1.3.2.2",
			"id_extension": hl7message['OBR.F18'] + hl7message['ZEI.F1'],
			"code": hl7message['OBR.F4.R1.C1'],
			"codeSystem": "1.3.6.1.4.1.55196.2.1",
			"codeSystemName": "Tabela MDCT - Imagiologia",
			"displayName": hl7message['OBR.F4.R1.C2'],
		}

		# documentationOf
		# TODO: To implement
		# self.m_documentationOf = {
		# 	"classCode": "ACT",
		# 	"id_root": "1.2.826.0.1.5968184.2.2.1.1555065954200.9891",
		# 	"code": "11010",
		# 	"codeSystem": "SAUDACOR.PROCEDURES",
		# 	"codeSystemName": "Saudacor Procedures",
		# 	"displayName": "ABDÓMEN SIMPLES, UMA INCIDÊNCIA",
		# 	"effectiveTime": "20190902120127+0000",
		# }

		# authorization
		# TODO: To implement

		# relatedDocument
		# TODO: To implement

		# componentOf
		# TODO: To implement

		# CONF-DIR-102: The templateId for a Findings section SHALL be 2.16.840.1.113883.10.20.6.1.2.
		self.m_cdaBody_Sections = [
			{
				"templateId": "2.16.840.1.113883.10.20.6.1.2",
				"code": "18782-3",
				"codeSystem": "2.16.840.1.113883.6.1",
				"codeSystemName": "LOINC",
				"displayName": "RADIOLOGY STUDY OBSERVATION",
				"title": "Observação",
				"text": hl7message['OBX.F5']
			},
			{
				"templateId": "",
				"code": "11329-0",
				"codeSystem": "2.16.840.1.113883.6.1",
				"codeSystemName": "LOINC",
				"displayName": "HISTORY GENERAL",
				"title": "Informação Clínica",
				"text": hl7message['OBR.F13']
			}
		]


###################################################################
## End of Main configuration
###################################################################
