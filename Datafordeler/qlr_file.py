from builtins import object
from qgis.core import *
from qgis.PyQt import QtXml
import os
import urllib.parse
import urllib.request, urllib.parse, urllib.error
from qgis.PyQt import QtCore

class QlrFile(object):

    def __init__(self, xml):
        try:
            self.doc = QtXml.QDomDocument()
            self.doc.setContent(xml)
        except Exception as e:
            b= 3

    def get_groups_with_layers(self):
        #result: [{'name': groupName, 'layers': [{'name': layerName, 'id': layerId}]}]
        result = []
        groups = self.doc.elementsByTagName("layer-tree-group")
        i = 0
        while i<groups.count():
            group = groups.at(i)
            group_name = None
            if group.toElement().hasAttribute("name") and group.toElement().attribute("name") != '':
                group_name = group.toElement().attribute("name")
                layers = self.get_group_layers(group)
                if layers and group_name:
                    result.append({'name': group_name, 'layers': layers})
            i += 1
        return result

    def get_group_layers(self, group_node):
        #result:[{'name': layerName, 'id': layerId}]
        result = []
        child_nodes = group_node.childNodes()
        i = 0
        while i<child_nodes.count():
            node = child_nodes.at(i)
            if node.nodeName() == "layer-tree-layer":
                layer_name = node.toElement().attribute("name")
                layer_id = node.toElement().attribute("id")
                maplayer_node = self.get_maplayer_node(layer_id)
                if maplayer_node:
                    service = self.get_maplayer_service(maplayer_node)
                    if service:
                        result.append({'name': layer_name, 'id': layer_id, 'service': service})
            i += 1
        return result
    
    def get_maplayer_service(self, maplayer_node):
        service = 'other'
        datasource_node = None
        datasource_nodes = maplayer_node.toElement().elementsByTagName('datasource')
        if datasource_nodes.count() == 1:
            datasource_node = datasource_nodes.at(0) 
            datasource = datasource_node.toElement().text()
            url_part = None
            datasource_parts = datasource.split('&') + datasource.split(' ') 
            #datasource_parts.append(datasource.split(' '))
            for part in datasource_parts:
                if part.startswith('url'):
                    url_part = part
            if url_part:
                if url_part:
                    #url = url_part.split('=')[1]
                    url = url_part[5:]
                    url = urllib.parse.unquote(url)
                    url_params = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
                    if 'servicename' in url_params:
                        service = url_params['servicename']
        return service

    def get_maplayer_node(self, id):
        node = self.getFirstChildByTagNameValue(
            self.doc.documentElement(), 'maplayer', 'id', id
        )
        return node 

    def getFirstChildByTagNameValue(self, elt, tagName, key, value):
        nodes = elt.elementsByTagName(tagName)
        i = 0
        while i < nodes.count():
            node = nodes.at(i)
            idNode = node.namedItem(key)
            if idNode is not None:
                child = idNode.firstChild().toText().data()
                # layer found
                if child == value:
                    return node
            i += 1
        return None
        

        
        
    