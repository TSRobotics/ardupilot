#!/usr/bin/env python

from __future__ import print_function

from lxml import etree
import emitter

class XMLEmitter(emitter.Emitter):
    def preface(self):
        return """<?xml version="1.0" encoding="utf-8"?>
<!-- Dynamically generated list of documented logfile messages (generated by parse.py) -->
"""

    def postface(self):
        return

    def start(self):
        self.logname = "LogMessages.xml"
        self.fh = open("LogMessages.xml", mode='w')
        print(self.preface(), file=self.fh)
        self.loggermessagefile = etree.Element('loggermessagefile')

    def emit(self, doccos):
        self.start()
        for docco in doccos:
            xml_logformat = etree.SubElement(self.loggermessagefile, 'logformat', name=docco.name)
            if docco.url is not None:
                xml_url = etree.SubElement(xml_logformat, 'url')
                xml_url.text = docco.url
            if docco.description is not None:
                xml_description = etree.SubElement(xml_logformat, 'description')
                xml_description.text = docco.description

            xml_fields = etree.SubElement(xml_logformat, 'fields')
            for f in docco.fields_order:
                xml_field = etree.SubElement(xml_fields, 'field', name=f)
                if "description" in docco.fields[f]:
                    xml_description2 = etree.SubElement(xml_field, 'description')
                    xml_description2.text = docco.fields[f]["description"]
                if "bits" in docco.fields[f]:
                    xml_bits = etree.SubElement(xml_field, 'bits')
                    xml_bits.text = docco.fields[f]["bits"]
            if xml_fields.text is None and not len(xml_fields):
                xml_fields.text = '\n'  # add </param> on next line in case of empty element.
        self.stop()

    def stop(self):
        # etree.indent(self.loggermessagefile)  # not available on thor, Ubuntu 16.04
        pretty_xml = etree.tostring(self.loggermessagefile, pretty_print=True, encoding='unicode')
        self.fh.write(pretty_xml)
        self.fh.close()