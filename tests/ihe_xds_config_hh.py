###################################################################
## Main configuration
###################################################################


	# These are the following fields that should go into an XDS document submission request
	# Metadata Element 	Metadata Attribute 	XDS DS
	# DocumentEntry		author					R2
	# DocumentEntry		availabilityStatus		O
	# DocumentEntry		classCode				R
	# DocumentEntry		comments				O
	# DocumentEntry		confidentialityCode		R
	# DocumentEntry		creationTime			R
	# DocumentEntry		entryUUID				R
	# DocumentEntry		eventCodeList			O
	# DocumentEntry		formatCode				R
	# DocumentEntry		hash					O
	# DocumentEntry		healthcareFacilityTypeCode		R
	# DocumentEntry		homeCommunityId			O
	# DocumentEntry		languageCode			R
	# DocumentEntry		legalAuthenticator		O
	# DocumentEntry		limitedMetadata			X
	# DocumentEntry		mimeType				R
	# DocumentEntry		objectType				R
	# DocumentEntry		patientId				R
	# DocumentEntry		practiceSettingCode		R
	# DocumentEntry		referenceIdList			O
	# DocumentEntry		repositoryUniqueId		O
	# DocumentEntry		serviceStartTime		R2
	# DocumentEntry		serviceStopTime			R2
	# DocumentEntry		size					O
	# DocumentEntry		sourcePatientId			R
	# DocumentEntry		sourcePatientInfo		O
	# DocumentEntry		title					O
	# DocumentEntry		typeCode				R
	# DocumentEntry		uniqueId				R
	# DocumentEntry		URI						O

	# SubmissionSet		author					R2
	# SubmissionSet		availabilityStatus		O
	# SubmissionSet		comments				O
	# SubmissionSet		contentTypeCode			R
	# SubmissionSet		entryUUID				R
	# SubmissionSet		homeCommunityId			O
	# SubmissionSet		intendedRecipient		O
	# SubmissionSet		limitedMetadata			X
	# SubmissionSet		patientId				R
	# SubmissionSet		sourceId				R
	# SubmissionSet		submissionTime			R
	# SubmissionSet		title					O
	# SubmissionSet		uniqueId				R

	# Folder is not implemented
	# Folder			availabilityStatus		O
	# Folder			codeList				R
	# Folder			comments				O
	# Folder			entryUUID				R
	# Folder			homeCommunityId			O
	# Folder			lastUpdateTime			O
	# Folder			limitedMetadata			X
	# Folder			patientId				R
	# Folder			title					R
	# Folder			uniqueId				R


	# In order to create coded attributes in the function below:
	# 1. Code Value – contains the assigned value of the code.
	# 2. Code Display Name - The display name used to represent the code (code values are not
	# necessarily human-friendly). Must be non-zero length.
	# 3. Coding Scheme - An identifier of the coding scheme that the code comes from.
	# For common Coding Schemes, see DICOM PS3.16, Table 8-1 Coding Schemes
	# (http://dicom.nema.org/medical/dicom/current/output/chtml/part16/chapter_8.html).
	# • If the Code Value is from a Coding Scheme in this table, the value for Coding
	# Scheme should be taken from either the “Coding Scheme UID” or the “Coding
	# Scheme Designator” column. If both are available, the value of Coding Scheme UID
	# should be used.
	# • If the Code Value is from a Coding Scheme that is not in this table, and if the Coding
	# Scheme can be identified with an OID, then the OID should be used.
	#
	# Taking information from HL7 message:
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
	def fill_xds_metadata(self, hl7message):
		# The humans and/or machines that authored the document. This attribute contains the sub-
		# attributes: authorInstitution, authorPerson, authorRole, authorSpecialty and
		# authorTelecommunication. See ITI TF-3:4.2.3.1.4 Creating Author Attributes
		# authorPerson – zero or one
		# authorInstitution – zero or more
		# authorRole – zero or more
		# authorSpecialty – zero or more
		# authorTelecommunication – zero or more
		#
		# Required if known
		#
		# There may be multiple authors
		# There may be multiple authorvalue
		# authorrole can be one of authorInstitution, authorPerson, authorRole,
		#     authorSpecialty or authorTelecommunication
		# Implemented as an array of authors that contain a dictionary, which can have
		# multiple values for the authorvalue as array
		# one complete example of the whole structure might be:
		# self.m_DocumentEntry_author = [[
		# 	{
		# 		"authorvalue": ["^Smitty^Gerald^^^"],
		# 		"authorrole": "authorPerson",
		# 	},
		# 	{
		# 		"authorvalue": ["Cleveland Clinic", "Berea Community"],
		# 		"authorrole": "authorInstitution",
		# 	},
		# 	{
		# 		"authorvalue": ["Attending"],
		# 		"authorrole": "authorRole",
		# 	},
		# 	{
		# 		"authorvalue": ["Orthopedic"],
		# 		"authorrole": "authorSpecialty",
		# 	}
		# ], [
		# 	{
		# 		"authorvalue": ["^Dopplemeyer^Sherry^^^"],
		# 		"authorrole": "authorPerson",
		# 	},
		# 	{
		# 		"authorvalue": ["Cleveland Clinic", "Parma Community"],
		# 		"authorrole": "authorInstitution",
		# 	},
		# 	{
		# 		"authorvalue": ["Primary Surgeon"],
		# 		"authorrole": "authorRole",
		# 	},
		# 	{
		# 		"authorvalue": ["Orthopedic"],
		# 		"authorrole": "authorSpecialty",
		# 	}
		# ]]
		self.m_DocumentEntry_author = [[
			{
				"authorvalue": [hl7message['OBR.F32.R1.C1.S2']],
				"authorrole": "authorPerson",
			},
			{
				"authorvalue": ["Hospital da Horta - Departamento de Radiologia"],
				"authorrole": "authorInstitution"
			}
		]]


		# Represents the status of the DocumentEntry. A DocumentEntry shall have one of two availability
		# statuses:
		#	Approved The document is available for patient care.
		#	Deprecated The document is obsolete.
		#
		# Optional
		# 
		self.m_DocumentEntry_availabilityStatus = ""
		# self.m_DocumentEntry_availabilityStatus = "urn:oasis:names:tc:ebxml-regrep:StatusType:Approved"
		# self.m_DocumentEntry_availabilityStatus = "urn:oasis:names:tc:ebxml-regrep:StatusType:Deprecated"


		# The code specifying the high-level use classification of the document type (e.g., Report,
		# Summary, Images, Treatment Plan, Patient Preferences, Workflow). The typeCode specifies the
		# precise type of document from the user perspective. Valid values for classCode attribute are
		# specified by the policies of the creating entity. It is recommended that the creating entity draws
		# these values from a coding scheme providing a coarse level of granularity (about 10 to 100
		# entries). For example, XDS specifies that the XDS Affinity Domain will establish this list.
		# There shall be exactly zero or one ebRIM Classification containing a classCode for any
		# DocumentEntry
		#
		# Required
		#
		self.m_DocumentEntry_classCode = {
			"codeValue": "REPORTS",
			"codeDisplayName": "Relatório de Imagiologia",
			"codingScheme": "1.3.6.1.4.1.19376.1.2.6.1"
		}


		# Contains comments associated with the document.
		#
		# Optional
		#
		self.m_DocumentEntry_comments = ""
		# self.m_DocumentEntry_comments = "comment associated with the Document"


		# The code specifying the security and privacy tags of the document. These codes are set by policy
		# of the participants in the exchange, e.g., XDS affinity domain. confidentialityCode is part of a
		# codification scheme.
		# [1...1] Confidentiality Security Classification Label Field
		# [0...*] Sensitivity Security Category Label Field
		# [0...*] Compartment Security Category Label Field
		# [0...*] Integrity Security Category Label Field
		# [0...*] Handling Caveat Security Category Field
		#
		# Required
		#
		self.m_DocumentEntry_confidentialityCode = {
			"codeValue": "N",
			"codeDisplayName": "Normal Clinical Data",
			"codingScheme": "2.16.840.1.113883.5.25"
		}


		# Represents the time the author created the document
		#
		# Required
		#
		# import datetime
		# current_date = datetime.datetime.utcnow()
		# self.m_DocumentEntry_creationTime =  current_date.strftime("%Y%m%d%H%M%S")
		# self.m_DocumentEntry_creationTime = "20051224"
		self.m_DocumentEntry_creationTime = hl7message['OBR.F22']


		# The entryUUID attribute is a globally unique identifier primarily intended for internal document
		# management purposes. In contrast, the uniqueId attribute is used for external references (e.g.,
		# links, etc.).
		#
		# Required
		#
		self.m_DocumentEntry_entryUUID = "Document01"
		# self.m_DocumentEntry_entryUUID = "urn:uuid:{}".format(uuid.uuid1())


		# This list of codes represents the main clinical acts, such as a colonoscopy or an appendectomy,
		# being documented. In some cases, the event is inherent in the typeCode, such as a "History and
		# Physical Report" in which the procedure being documented is necessarily a "History and
		# Physical" act. An event can further specialize the act inherent in the typeCode, such as where it is
		# simply "Procedure Report" and the procedure was a "colonoscopy". When defining the value sets
		# for eventCodes, they should not conflict with the values inherent in the classCode,
		# practiceSettingCode or typeCode as such a conflict would create an ambiguous situation.
		#
		# Optional
		#
		self.m_DocumentEntry_eventCodeList = ""
		# self.m_DocumentEntry_eventCodeList = {
		#	"codeValue": "ExampleeventCode",
		#	"codeDisplayName": "eventCodeDisplayName",
		#	"codingScheme": "Example Event Code Scheme"
		# }


		# The code specifying the detailed technical format of the document. Along with the typeCode, it
		# should provide sufficient information to allow potential consumer to know if it will be able to
		# process the document.
		# The mimeType indicates the base format; the formatCode indicates the detailed-level technical
		# structure. Together with the mimeType, the formatCode used shall be sufficiently specific to
		# ensure processing/display by identifying a document encoding, structure and template (e.g., for a
		# CDA Document, the fact that it complies with a CDA schema, possibly a template and the choice
		# of a content-specific style sheet). The formatCode alone is often sufficiently specific, but an
		# actor that consumes metadata should not assume that it is.
		# The formatCode is often an indicator of the IHE Document Content Profile to which the
		# document conforms.
		# The mimeTypeSufficient formatCode of EV("urn:ihe:iti:xds:2017:mimeTypeSufficient",
		# "1.3.6.1.4.1.19376.1.2.3") may be used when the mimeType is sufficient to identify the technical
		# format of the document.
		# Format codes may be specified by multiple organizations. Format codes for Document Content
		# Profiles defined by the ITI domain shall be in URN format and have names with the prefix
		# urn:ihe:iti:
		# Format codes defined by other IHE domains shall have names with the prefix
		# urn:ihe:’domain initials’:
		# The IHE-managed codes and value set for formatCode are published on
		# http://wiki.ihe.net/index.php/IHE_Format_Codes.
		# Format codes defined by non-IHE domains should be a valid unique URN.
		#
		# Required
		#
		self.m_DocumentEntry_formatCode = {
			"codeValue": "urn:ihe:iti:xds:2017:mimeTypeSufficient",
			"codeDisplayName": "mimeType Sufficient",
			"codingScheme": "1.3.6.1.4.1.19376.1.2.3"
		}


		# The hash of the contents of the document.
		# The hash attribute can be used to identify accidental document corruption, mistaken duplicate
		# IDs, etc. The SHA1 algorithm and hash attribute should not be used for identifying malicious
		# alterations.
		#
		# Optional
		#
		# Does not require a value here as it is received as argument
		# self.m_DocumentEntry_hash


		# This code represents the type of organizational setting of the clinical encounter during which the
		# documented act occurred.
		# In some cases, the setting of the encounter is inherent in the typeCode, such as "Diabetes Clinic
		# Progress Note". healthcareFacilityTypeCode shall be equivalent to or further specialize the value
		# inherent in the typeCode; for example, where the typeCode is simply "Clinic Progress Note" and
		# the value of healthcareFacilityTypeCode is "private clinic".
		#
		# Required
		#
		# self.m_DocumentEntry_healthcareFacilityTypeCode = {
		#	"codeValue": "HOSP",
		#	"codeDisplayName": "Hospital",
		#	"codingScheme": "2.16.840.1.113883.4.642.2.246"
		# }
		self.m_DocumentEntry_healthcareFacilityTypeCode = {
			"codeValue": "22232009",
			"codeDisplayName": "Hospital",
			"codingScheme": "2.16.840.1.113883.6.96"
		}


		# A globally unique identifier for a community where the DocumentEntry and document can be
		# accessed.
		#
		# Optional
		#
		self.m_DocumentEntry_homeCommunityId = ""
		# self.m_DocumentEntry_homeCommunityId = "urn:oid:1.2.3"


		# Specifies the human language of character data in the document
		#
		# Required
		#
		self.m_DocumentEntry_languageCode = "pt-PT"


		# Represents a participant within an authorInstitution who has legally authenticated or attested the
		# document. Legal authentication implies that a document has been signed manually or
		# electronically by the legalAuthenticator.
		# XCN format
		#
		# Optional
		#
		# legalAuthenticator shall be in XCN format
		self.m_DocumentEntry_legalAuthenticator = ""
		# self.m_DocumentEntry_legalAuthenticator = "^Welby^Marcus^^^Dr^MD"


		# Indicates whether the Document Entry was created using the less rigorous requirements of
		# metadata as defined for the Metadata-Limited Document Source Actor.
		#
		# Forbidden
		#
		# global self.m_DocumentEntry_limitedMetadata
		# self.m_DocumentEntry_limitedMetadata = Forbidden


		# MIME type of the document in the Repository
		#
		# Required
		#
		self.m_DocumentEntry_mimeType = "text/xml"


		# The objectType attribute reflects the type of DocumentEntry. As described in Section 4.1.1, there
		# are two DocumentEntry types: Stable Document Entry and On-Demand Document Entry. A
		# Stable Document Entry contains metadata about an already created document available for
		# retrieval is a Document Entry and is designated by setting objectType equal to the UUID for
		# Stable (see Section 4.2.5.2 for the UUID). An On-Demand Document Entry contains metadata
		# which can be used to create an on-demand document which collects the latest, most recent
		# available information at the time of retrieval. It is designed by setting an objectType equal to the
		# UUID for on-demand (see Section 4.2.5.2 for the UUID).
		# The value of the objectType is coded in the objectType XML attribute on the ExtrinsicObject
		# representing the DocumentEntry. In the example below, the objectType is urn:uuid:7edca82f-
		# 054d-47f2-a032-9b2a5b5186c1 and reflects a stable DocumentEntry.
		#
		# Required
		#
		# Stable Document Entry
		self.m_DocumentEntry_objectType = "urn:uuid:7edca82f-054d-47f2-a032-9b2a5b5186c1"
		# On-Demand Document Entry
		# self.m_DocumentEntry_objectType = "urn:uuid:34268e47-fdf5-41a6-ba33-82133c465248"


		# This call finds the PID-3 repetition that has the patient ID in the 
		# XDS affinity domain
		# Use this variable instead of "repetition" in the HL7 message
		xad_pid_repetition = hl7_v2x_receiver.Hl7v2x.hl7_find_xad_pid_repetition(hl7message)


		# The patientId represents the subject of care of the document. For XDS the patient identifier
		# domain is the XDS Affinity Domain Patient Identifier Domain (XAD-PID).
		# Within a submission request, the value of patientId of the DocumentEntries shall match that of
		# the SubmissionSet
		# The format of the patientId value is CX; see Table 4.2.3.1.7-2.
		# It shall contain two parts:
		# • Assigning Authority Domain Id (organization that issued the Id)
		# • An Id from the above Assigning Authority.
		# No other values are allowed, as specified for the CX type. Using HL7 terminology, no other
		# values are allowed in the components of the coded value, nor are further subcomponents
		# allowed.
		#
		# Required
		#
		# Patient ID in CX format
		# self.m_DocumentEntry_patientId = "6578946^^^&1.3.6.1.4.1.21367.2005.3.7&ISO"
		self.m_DocumentEntry_patientId = hl7message.unescape(
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(1)) +
			"^^^&" +
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(4)(2)) +
			"&" +
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(4)(3))
		)


		# The code specifying the clinical specialty where the act that resulted in the document was
		# performed (e.g., Family Practice, Laboratory, Radiology). It is suggested that the creating entity
		# draws these values from a coding scheme providing a coarse level of granularity (about 10 to 100
		# entries).
		#
		# Required
		#
		# This attribute shall be populated by the Imaging Document Source to
		# describe the high-level imaging specialty such as (R-3027B, SRT,
		# “Radiology”), (R-3026B, SRT, “Pathology”), or (R-30248, SRT,
		# “Cardiology”). The list of acceptable values is constrained by the
		# organization managing the XDS Registry (i.e., the XDS Affinity
			# Domain).
		# It is strongly recommended to use the values from the DICOM Content
		# Mapping Resource (PS3.16) Context Group CID 7030.
		# http://dicom.nema.org/medical/dicom/current/output/html/part16.html#sect_CID_7030
		# self.m_DocumentEntry_practiceSettingCode = {
		#	"codeValue": "441662001",
		#	"codeDisplayName": "Diagnostic Imaging",
		#	"codingScheme": "2.16.840.1.113883.6.96"
		# }
		self.m_DocumentEntry_practiceSettingCode = {
			"codeValue": "R-3027B",
			"codeDisplayName": "Radiology",
			"codingScheme": "2.16.840.1.113883.6.96"
		}


		# These Identifiers may be internal or external identifiers, e.g., Identifiers may be Accession
		# Numbers, Order Numbers, Referral Request Identifiers, XDW Workflow Instance Identifiers,
		# etc. The referenceIdList contains Identifiers CXi encoded, as specified in Table 4.2.3.1.7-2.
		# Max length is 256 characters.
		# Coded as an ebRIM Slot. May have multiple values.
		#
		# Optional
		#
		# self.m_DocumentEntry_referenceIdList = ""
		# A simple array of external identifiers
		self.m_DocumentEntry_referenceIdList = [
			hl7message['OBR.F18'] + "^^^^urn:ihe:iti:xds:2013:accession"
		]
		# self.m_DocumentEntry_referenceIdList = [ "1.2.3.12.78.23^^^&1.2.3.4&ISO^urn:ihe:iti:xds:2013:uniqueId" ]
		# TODO: Why sectra uses also urn:sectra:iti:xds:2015:referenceAndStudyIdList


		# The globally unique, immutable, identifier of the repository where the document referenced by
		# the Document Entry can be accessed. This unique identifier for the repository may be used to
		# identify and connect to the specific repository to access the document
		#
		# Optional
		#
		# Identifier of the repository where the document referenced by
		# the Document Entry can be accessed.
		self.m_DocumentEntry_repositoryUniqueId = ""
		# self.m_DocumentEntry_repositoryUniqueId = "1.3.6.1.4.5"


		# Represents the start time of the service being documented (clinically significant, but not
		# necessarily when the document was produced or approved). This may be the same as the
		# encounter time in case the service was delivered during an encounter. Encounter time is not
		# coded in metadata but may be coded within the document.
		# Note: If needed, other times associated with the document, such as time of approval, are to be
		# recorded within the document.
		# The format of serviceStartTime value is DTM
		#
		# Required if known
		#
		# The format of the serviceStartTime value is DTM
		# self.m_DocumentEntry_serviceStartTime = "200412230800"
		self.m_DocumentEntry_serviceStartTime = hl7message['OBR.F22']


		# Represents the stop time of the service being documented (clinically significant, but not
		# necessarily when the document was produced or approved). This may be the same as the
		# encounter time in case the service was delivered during an encounter. Encounter time is not
		# coded in metadata but may be coded within the document.
		# If the service happens at a point in time, this attribute shall contain the same value as the
		# serviceStartTime.
		# The format of serviceStopTime value is DTM
		#
		# Required if known
		#
		# The format of the serviceStopTime value is DTM
		# self.m_DocumentEntry_serviceStopTime = "200412230801"
		self.m_DocumentEntry_serviceStopTime = hl7message['OBR.F22']


		# Size in bytes of the byte stream that comprises the document
		#
		# Optional
		#
		# Does not require a value for self.m_DocumentEntry_size as it is received as argument
		# self.m_DocumentEntry_size


		# The sourcePatientId represents the subject of care’s medical record identifier (e.g., Patient Id) in
		# the local patient identifier domain of the creating entity.
		# Coded as an ebRIM Slot with the value encoded according the CX
		# datatype (see Table 4.2.3.1.7-2)
		#
		# Required
		#
		# self.m_DocumentEntry_sourcePatientId = "j98789^^^&1.2.3.4.343.1&ISO"
		self.m_DocumentEntry_sourcePatientId = hl7message.unescape(
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(1)) +
			"^^^&" +
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(4)(2)) +
			"&" +
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(4)(3))
		)


		# This attribute contains demographics information at the time of submission of the patient to
		# whose medical record this document belongs.
		# This information typically includes: the patient first and last name, sex, and birth date. Policies at
		# the creating entity may require more or less specific information and format.
		# This patient information is not intended to be updated once the document is registered (just as the
		# document content and metadata itself will not be updated without replacing the previous
		# document). As sourcePatientInfo may have been updated by the source actor, it may no longer be
		# in use within the Document Source (EHR-CR). It is only intended as an audit/checking
		# mechanism and has occasional use for Document Consumer Actors.
		# Coding:
		# Coded as an ebRIM Slot. If present, each rim:Value contains a Field (see Table 4.2.3.1.7-2 for a
		# description of the Field datatype). Multiple rim:Value elements may exist for the same field
		# name as a way to implement repetition; there shall be at most one rim:Value element for each of
		# the PID-7 and PID-8 fields. Only field defined for the PID segment shall be used.
		# Maximum length of each rim:Value is 256 characters. The sourcePatientInfo attribute should
		# include:
		# • PID-3 (source patient identifier list)
		# • PID-5 (source patient name)
		# • If multiple patient names are present, then PID-5.7 “Name Type Code” and PID-5.8
		#   “Name Representation Code” should be valued in each entry.
		# • PID-7 (source patient date of birth)
		# • PID-8 (source patient gender)
		# The sourcePatientInfo attribute should not include values for PID-2 (patient id), PID-4 (alternate
		# patient id), PID-12 (country code), or PID-19 (social security number).
		#
		# Optional
		#
		# sourcePatientInfo should be an array of values, 
		# PID-3 (source patient identifier list)
		# PID-5 (source patient name)
		# If multiple patient names are present, then PID-5.7 “Name Type Code” and PID-5.8
		#     “Name Representation Code” should be valued in each entry.
		# PID-7 (source patient date of birth)
		# PID-8 (source patient gender)
		# self.m_DocumentEntry_sourcePatientInfo = ""
		# self.m_DocumentEntry_sourcePatientInfo = [
		# 	"PID-3|D\E\ID1-1^^^&1.3.6&ISO~ID2^^^&1.3.11&ISO",
		# 	"PID-3|YZP-2^^^&1.3.42&ISO~ABC-3^^^&1.3.3.14&ISO",
		# 	"PID-5|DICTAPHONE^ONE^^^",
		# 	"PID-7|19650120",
		# 	"PID-8|M",
		# 	"PID-11|100 Main St^^BURLINGTON^MA^01803^USA"
		# ]
		# Adds all patient domain ids into a list
		# TODO: Sending many PID-3 is currently not working for XDS toolkit
		# TODO: But i think it would be acceptable from the description above
		self.m_DocumentEntry_sourcePatientInfo = []
		for domain_id in range(1, len(hl7message.segment('PID')(3)) + 1):
			self.m_DocumentEntry_sourcePatientInfo.append("PID-3|" +
				hl7message.unescape(
					str(hl7message.segment('PID')(3)(domain_id)(1)) +
					"^^^&" +
					str(hl7message.segment('PID')(3)(domain_id)(4)(2)) +
					"&" +
					str(hl7message.segment('PID')(3)(domain_id)(4)(3))
				)
			)
		# Adds remaining sourcePatientInfo
		self.m_DocumentEntry_sourcePatientInfo.append("PID-5|" + hl7message.unescape(str(hl7message.segment('PID')(5))))
		self.m_DocumentEntry_sourcePatientInfo.append("PID-7|" + hl7message['PID.F7'])
		self.m_DocumentEntry_sourcePatientInfo.append("PID-8|" + hl7message['PID.F8'])


		# Represents the title of the document.
		# Clinical documents often do not have a title; in such case the classCode (e.g., a "consultation" or
		# "progress note") is often used as the title. In that case, the title is usually omitted.
		#
		# Optional
		#
		# self.m_DocumentEntry_title = "Example Document Title"
		self.m_DocumentEntry_title = ""


		# The code specifying the precise type of document from the user’s perspective. It is recommended
		# that the creating entity draw these values from a coding scheme providing a fine level of
		# granularity such as LOINC.
		#
		# Required
		#
		# The exam code
		self.m_DocumentEntry_typeCode = {
			"codeValue": "18748-4",
			"codeDisplayName": "Diagnostic Imaging Study",
			"codingScheme": "2.16.840.1.113883.6.1"
		}


		# Globally unique identifier assigned to the document by its creator
		# See section 4.2.3.2.26 DocumentEntry.uniqueId in ITI TF-3
		#
		# Required
		#
		# https://wiki.ihe.net/index.php/Creating_Unique_IDs_-_OID_and_UUID
		# an OID from an UUID must start with "2.25." and followed by the straight decimal encoding of the UUID as an integer
		self.m_DocumentEntry_uniqueId = {
			"value": "2.25.{}".format(uuid.uuid1().int),
			"codeDisplayName": "XDSDocumentEntry.uniqueId",
		}


		# The URI attribute contains the URI for the document.
		# Max length is 256 characters. Coded as an ebRIM Slot. Shall have only a single value.
		#
		# Optional
		#
		self.m_DocumentEntry_URI = ""
		# self.m_DocumentEntry_URI = "DOC001.XML"


		###############################################################################


		# Represents the humans and/or machines that authored the SubmissionSet. See Section 4.2.3.1.4
		# for details on creating the structure.
		# authorPerson – zero or one
		# authorInstitution – zero or more
		# authorRole – zero or more
		# authorSpecialty – zero or more
		# authorTelecommunication – zero or more
		#
		# Required if known
		#
		# There may be multiple authors
		# There may be multiple authorvalue
		# authorrole can be one of authorInstitution, authorPerson, authorRole,
		#     authorSpecialty or authorTelecommunication
		# Implemented as an array of authors that contain a dictionary, which can have
		# multiple values for the authorvalue as array
		# self.m_SubmissionSet_author = [[
		# 	{
		# 		"authorvalue": ["^Dopplemeyer^Sherry^^^"],
		# 		"authorrole": "authorPerson",
		# 	},
		# 	{
		# 		"authorvalue": ["Cleveland Clinic", "Berea Community"],
		# 		"authorrole": "authorInstitution",
		# 	},
		# 	{
		# 		"authorvalue": ["Primary Surgeon"],
		# 		"authorrole": "authorRole",
		# 	},
		# 	{
		# 		"authorvalue": ["Orthopedic"],
		# 		"authorrole": "authorSpecialty",
		# 	}
		# ]]
		self.m_SubmissionSet_author = [[
			{
				"authorvalue": [hl7message['OBR.F32.R1.C1.S2']],
				"authorrole": "authorPerson",
			},
			{
				"authorvalue": ["Hospital da Horta - Departamento de Radiologia"],
				"authorrole": "authorInstitution"
			}
		]]


		# Represents the status of the SubmissionSet. Since the deprecation of SubmissionSets is not
		# allowed, this value shall always be Approved.
		#
		# Optional
		#
		# Does not need to be implemented
		# Since the deprecation of SubmissionSets is not allowed, this value shall always be Approved.
		# self.m_SubmissionSet_availabilityStatus


		# Contains comments associated with the SubmissionSet
		#
		# Optional
		#
		# self.m_SubmissionSet_comments = "Annual physical"
		self.m_SubmissionSet_comments = ""


		# The code specifying the type of clinical activity that resulted in placing these DocumentEntries,
		# Folders, and/or Associations in this SubmissionSet. These values are to be drawn from a
		# vocabulary defined by the creating entity that contributed the SubmissionSet.
		#
		# Required
		#
		self.m_SubmissionSet_contentTypeCode = {
			"codeValue": hl7message['OBR.F4.R1.C1'],
			"codeDisplayName": hl7message['OBR.F4.R1.C2'],
			"codingScheme": hl7message['OBR.F4.R1.C3']
		}


		# The entryUUID attribute is a globally unique identifier primarily intended for internal document
		# management purposes. In contrast, the uniqueId attribute is used for external references (e.g.,
		# links, etc.).
		#
		# Required
		#
		# self.m_SubmissionSet_entryUUID = "urn:uuid:{}".format(uuid.uuid1())
		self.m_SubmissionSet_entryUUID = "SubmissionSet01"


		# A globally unique identifier for a community.
		#
		# Optional
		#
		self.m_SubmissionSet_homeCommunityId = ""
		# self.m_SubmissionSet_homeCommunityId = "urn:oid:1.2.3"


		# Represents the organization(s) or person(s) for whom the SubmissionSet is intended at time of
		# submission. Each slot value shall include at least one of the organization, person, or
		# telecommunications address fields described below. It is highly recommended to define the
		# organization for all the persons, avoiding errors in the transmission of the documents
		# The value is coded as zero or more values within a single ebRIM Slot in the SubmissionSet.
		#
		# Optional
		#
		self.m_SubmissionSet_intendedRecipient = ""
		# self.m_SubmissionSet_intendedRecipient = [
		#	"Some Hospital^^^^^^^^^1.2.3.9.1789.45|^Wel^Marcus^^^Dr^MD|^^Internet^mwel@healthcare.example.org",
		#	"Some Hospital^^^^^^^^^1.2.3.9.1789.45|^Peirre^LaPointe^^^Dr^MD",
		#	"|12345^LaShawn^James^^Dr^MD",
		#	"MainHospital^^^^^^^^^1.2.3.4.5.6.7.8.9.1789.2364",
		#	"^^Internet^dr.oz@healthcare.example.org"
		# ]


		# Indicates whether the SubmissionSet was created using the less rigorous requirements of
		# metadata as defined for the Metadata-Limited Document Source
		#
		# Forbidden
		#
		# self.m_SubmissionSet_limitedMetadata = Forbidden


		# The patientId represents the primary subject of care of the SubmissionSet
		# The format of the patientId value is CX (see Table 4.2.3.1.7-2)
		# It shall contain two parts:
		#    Assigning Authority Domain Id (organization that issued the Id).
		#    An Id from the above Assigning Authority.
		# No other values are allowed, as specified for the CX type. Using HL7 terminology, no other
		# values are allowed in the components of the coded value, nor are further subcomponents
		# allowed.
		#
		# Required
		#
		# self.m_SubmissionSet_patientId = "6578946^^^&1.3.6.1.4.1.21367.2005.3.7&ISO"
		self.m_SubmissionSet_patientId = hl7message.unescape(
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(1)) +
			"^^^&" +
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(4)(2)) +
			"&" +
			str(hl7message.segment('PID')(3)(xad_pid_repetition)(4)(3))
		)


		# The globally unique, immutable, identifier of the entity that contributed the SubmissionSet.
		# When a "broker" is involved in sending SubmissionSets from a collection of client systems, it
		# shall use a different sourceId for submissions from each separate system to allow for tracking.
		#
		# Required
		#
		self.m_SubmissionSet_sourceId = "1.3.6.1.4.1.55196.1.1.2.5"


		# Represents the point in time at the creating entity when the SubmissionSet was created
		# This shall be provided by the submitting system
		#
		# Required
		#
		# self.m_SubmissionSet_submissionTime should be filled with the time of submission
		# self.m_SubmissionSet_submissionTime = "20041225235050"
		import datetime
		current_date = datetime.datetime.utcnow()
		self.m_SubmissionSet_submissionTime =  current_date.strftime("%Y%m%d%H%M%S")


		# Shall contain the title of the SubmissionSet
		#
		# Optional
		#
		# self.m_SubmissionSet_title = "Example Submission Set Title"
		self.m_SubmissionSet_title = ""


		# The globally unique identifier for the SubmissionSet assigned by the entity that contributed the
		# SubmissionSet
		#
		# Required
		#
		# https://wiki.ihe.net/index.php/Creating_Unique_IDs_-_OID_and_UUID
		# an OID from an UUID must start with "2.25." and followed by the straight decimal encoding of the UUID as an integer
		self.m_SubmissionSet_uniqueId = "2.25.{}".format(uuid.uuid1().int)


		###############################################################################


		# Folder variables are not implemented


###################################################################
## End of Main configuration
###################################################################
