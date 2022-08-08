#!/usr/bin/python3
# -*- coding: utf-8 -*-

m_SubmissionSet_author = [[
	{
		"authorvalue": ["^Dopplemeyer^Sherry^^^"],
		"authorrole": "authorPerson",
	},
	{
		"authorvalue": ["Cleveland Clinic", "Berea Community"],
		"authorrole": "authorInstitution",
	},
	{
		"authorvalue": ["Primary Surgeon"],
		"authorrole": "authorRole",
	},
	{
		"authorvalue": ["Orthopedic"],
		"authorrole": "authorSpecialty",
	}
]]

m_DocumentEntry_author = [[
	{
		"authorvalue": ["^Smitty^Gerald^^^"],
		"authorrole": "authorPerson",
	},
	{
		"authorvalue": ["Cleveland Clinic", "Parma Community"],
		"authorrole": "authorInstitution",
	},
	{
		"authorvalue": ["Attending"],
		"authorrole": "authorRole",
	},
	{
		"authorvalue": ["Orthopedic"],
		"authorrole": "authorSpecialty",
	}
], [
	{
		"authorvalue": ["^Dopplemeyer^Sherry^^^"],
		"authorrole": "authorPerson",
	},
	{
		"authorvalue": ["Cleveland Clinic", "Parma Community"],
		"authorrole": "authorInstitution",
	},
	{
		"authorvalue": ["Primary Surgeon"],
		"authorrole": "authorRole",
	},
	{
		"authorvalue": ["Orthopedic"],
		"authorrole": "authorSpecialty",
	}
]]

mylist= m_DocumentEntry_author
# mylist= m_SubmissionSet_author
print(len(mylist))
for author in mylist:
	print("Author:")
	# print("Author: {}".format(author))
	# print("Author role: {}".format(author["authorrole"]))
	for authorrole in author:
		print("    Author role: {}".format(authorrole["authorrole"]))
		# authorvalue is an array
		for authorvalue in authorrole["authorvalue"]:
			print("    Value: {}	".format(authorvalue))

