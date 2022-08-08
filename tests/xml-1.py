#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Antonio Martins (digiplan.pt@gmail.com)
#

from lxml import etree
from lxml.builder import ElementMaker
import os
import logging
###################################################################
## Global variables
###################################################################

# Logging facility
logger = logging.getLogger('oru2xds')

nsmap_xdsb = {'xdsb': 'urn:ihe:iti:xds-b:2007'}
xdsb_prefix = "{" + nsmap_xdsb['xdsb'] + "}"
nsmap_lcm =  {'lcm': 'urn:oasis:names:tc:ebxml-regrep:xsd:lcm:3.0'}
lcm_prefix = "{" + nsmap_lcm['lcm'] + "}"
nsmap_rim =  {'rim': 'urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0'}
rim_prefix = "{" + nsmap_rim['rim'] + "}"
nsmap_xop = {'xop': 'http://www.w3.org/2004/08/xop/include'}
xop_prefix = "{" + nsmap_xop['xop'] + "}"

def create_Document(attachment_id):
	# Create Document
	document = etree.Element(xdsb_prefix + "Document", nsmap = nsmap_xdsb)
	document.attrib['id'] = "Test_001"
	attachment = etree.SubElement(document, xop_prefix + "Include", nsmap = nsmap_xop)
	attachment.attrib['href'] = attachment_id
	return document

CD = etree.Element(xdsb_prefix +'ProvideAndRegisterDocumentSetRequest', nsmap = nsmap_xdsb)
E = ElementMaker(namespace = nsmap_lcm['lcm'], nsmap = nsmap_lcm)
CD.append(
	E.SubmitObjectsRequest(
#		create_RegistryObjectList()
	)
)
CD.append(
	create_Document("Attach_001")
)

etree.indent(CD, space = "    ")
# print(etree.tostring(CD, pretty_print = True, xml_declaration = True, encoding = 'utf-8'))
print(etree.tostring(CD, pretty_print = True, encoding = 'unicode'))

