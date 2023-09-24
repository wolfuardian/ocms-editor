#---------------------------------------------------------------------
# Licensed to NADI System Corp. under a Contributor Agreement.
# See https://www.nadi3docms.com/ for licensing details.
#
# OCMS XML Editor For Maya
# Copyright (c) 2022-2023 by Roy Yu  All rights reserved.
#
# roy.you@nadisystem.com
# https://www.linkedin.com/in/roy-yu-791202/
# Tool Concept:
# Sync XML To Network => Sync Model to Maya => Modify Model Position Or Adding Model to the scene  => Sync Data to the XML File
# ObjectID => SensorID
# --------------------------------------------------------------------
# The OCMS XML Editor For Maya toolkit is
#
# Copyright (c) 2022-2023 by Roy Yu
#
# By obtaining, using, and/or copying this software and/or its
# associated documentation, you agree that you have read, understood,
# and will comply with the following terms and conditions:
#
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted, provided that the above copyright notice appears in
# all copies, and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# NADI System Corp. or the author not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# NADI System Corp. AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANT-
# ABILITY AND FITNESS.  IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR
# BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
# DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
# --------------------------------------------------------------------
# public symbols
__all__ = [
    "OCMSMAYAElementTree",
    "OCMSMAYAElement",
    "OCMSMAYAETWrite",
]
_version = "1.0.0.1"
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM
import unicodedata,codecs
import maya.cmds as cmds
import maya.OpenMaya as om;
import io,os,os.path,getpass,datetime,re
import shutil #for copy file
#--- This Class Only Work with Element Tree ------------------------------------------------------------------------------------------------
class OCMSMAYAElementTree():

    def __init__(self):
        self.__class__.root=None # first node
        self.__class__.tag=None
        self.__class__.Version={}
        self.__class__.fP_elements=[]
        self.__class__.elements=[]


    def setroot(self,root):
        if cmds.objExists(root):
            self.root=root
            return self.root
        else:
            raise NameError


    def parse(self,root):
        if cmds.objExists(root):
            self.root=root
            self.GetElements(0)
            self.GetElements(1)
        else:
            raise NameError
        return self.fP_elements


    def getroot(self):
        if cmds.objExists(self.root):
            return self.root
        else:
            raise NameError


    def GetElements(self,mode=1):
        __elems=[]
        tags=[]
        _elems=self.__list_elements(mode)
        elem_int=0
        if bool(_elems):
            for elem in _elems:
                tags=self.__list_tags(elem)
                if bool(tags):
                    __elems.append(elem)
                else:
                    pass
            if mode==0:
                self.elements=__elems
            elif mode==1:
                self.fP_elements=__elems
            else:
                cmds.warning('The mode selected is out of range.\n')
        else:
            cmds.warning('There is no element to conform.\n')
        return __elems


    def __list_elements(self,mode=1):
        elems=[]
        _root=''
        if mode>1 or mode<0:
            cmds.warning('The mode selected is out of range.\n')
        else:
            if mode==0:
                elems=cmds.listRelatives(self.root,allDescendents=True,path=True,type='transform')
                _root=self.root
            elif mode==1:
                elems=cmds.listRelatives(self.root,allDescendents=True,fullPath=True,type='transform')
                _root=("|" + self.root)
            elems.reverse()
            elems.insert(0,_root)
        return elems


    def __list_tags(self,element):
        tags=[]
        attr=cmds.listAttr(element,userDefined=True,write=True)
        if bool(attr):
            for at in attr:
                if not cmds.attributeQuery(at,node=element,numberOfChildren=True)==None:
                    tags.append(at)
        else:
            pass
            #cmds.warning( 'There is no user defined attribute.\n')
        return tags


    def GetElementByType(self,type):
        elems=[]
        self.GetElements(1)
        if bool(self.fP_elements):
            for element in self.fP_elements:
                if cmds.attributeQuery('type',node=element,exists=True):
                    if cmds.getAttr((element + '.type'))==type:
                        elems.append(element)
        else:
            cmds.warning('There is no element to conform.\n')
        return elems


    #--------------------------------------------------------------------------
class OCMSMAYAElement(OCMSMAYAElementTree):


    def __init__(self):
        self.__class__.encode = ['utf-16','utf-8','big5','ascii','gbk','unicode']
        self.__class__.element=None
        self.__class__.tree=None


    def __parse_attrib(self,element):
        attr={}
        _get={}
        if cmds.objExists(element):
            tags=self.GetElementTag(element)
            if bool(tags):
                for tag in tags:
                    _get=self.__get_attrib(tag,element)
                    if bool(_get):
                        attr[tag.replace('_','.')]=_get
            else:
                cmds.warning('This element does not qualify to conform.\n')
        else:
            pass
        return attr


    def parentNode(self,element):
        return self.__element_parent(element)


    def __element_parent(self,element):
        node=cmds.listRelatives(element,allDescendents=True,fullPath=True,parent=True,type='transform')
        if bool(node):
            _parent=node[0]
        else:
            _parent=None
        return _parent


    def __get_attrib(self,tag,element):
        attr_dict={}
        value=''
        attr=cmds.attributeQuery(tag,node=element,listChildren=True)
        if bool(attr):
            for at in attr:
                value=cmds.getAttr((element + '.' + at))
                if bool(value):
                    if isinstance(value,float):
                        attr_dict[at.replace('_','')]=str(value)
                    else:
                        attr_dict[at.replace('_','')]=value
                else:
                    pass
        return attr_dict


    def _get_attr_transform(self,element,attr):
        _x=cmds.getAttr((element + '.' + attr + 'X'))
        _y=cmds.getAttr((element + '.' + attr + 'Y'))
        _z=cmds.getAttr((element + '.' + attr + 'Z'))
        return([_x,_y,_z])


    def __get_transform(self,element):
        __Transform={}
        __Transform['Transform']={'position':{},'rotation':{},'scale':{}}
        _t=self._get_attr_transform(element,'translate')
        if not _t[0]==0 or not _t[1]==0 or not _t[2]==0:
            __Transform['Transform']['position']={"x":str(_t[0]),"y":str(_t[1]),"z":str(_t[2])}
        else:
            del __Transform['Transform']['position']
        _r=self._get_attr_transform(element,'rotate')
        if not _r[0]==0 or not _r[1]==0 or not _r[2]==0:
            __Transform['Transform']['rotation']={"x":str(_r[0]),"y":str(_r[1]),"z":str(_r[2])}
        else:
            del __Transform['Transform']['rotation']
        _s=self._get_attr_transform(element,'scale')
        if not _s[0]==1 or not _s[1]==1 or not _s[2]==1:
            __Transform['Transform']['scale']={"x":str(_s[0]),"y":str(_s[1]),"z":str(_s[2])}
        else:
            del __Transform['Transform']['scale']
        return(__Transform)


    def __component(self,dict):
        _dict={'Component':{}}
        for key in dict.keys():
            _com=dict[key]
            if bool(_com):
                _dict['Component'].update({key:_com})
            else:
                pass
        return(_dict)


    def GetAttributes(self,element):
        attr_dict={}
        dict=self.__parse_attrib(element)
        _obj={'Object':dict['Object']}
        __obj=_obj['Object']
        if bool(__obj):
            attr_dict.update(_obj)

        _transform=self.__get_transform(element)
        __transform=_transform['Transform']

        if bool(__transform):
            attr_dict.update(_transform)

        del dict['Object']
        _com=self.__component(dict)

        if bool(_com):
            attr_dict.update(_com)

        return attr_dict


    def GetElementTag(self,element):
        tags=[]
        attr=cmds.listAttr(element,userDefined=True,write=True)
        if bool(attr):
            for at in attr:
                if not cmds.attributeQuery(at,node=element,numberOfChildren=True)==None:
                    tags.append(at)
            return tags
        else:
            #cmds.warning( 'There is no user defined attribute.\n')
            pass


        #-------------------------------------------------------------------------------------------------------------------------------
class OCMSMAYAETWrite():


    def __init__(self,_root):
        self.__class__.encode = ['utf-16','utf-8','big5','ascii','gbk','unicode']
        self.__class__.root_attr={'xmlns:xsd':'http://www.w3.org/2001/XMLSchema','xmlns:xsi':'http://www.w3.org/2001/XMLSchema-instance'}
        self.__class__.root_init=0
        self.__class__.version_init=0
        self.OCMSMAYAET=OCMSMAYAElement()
        self.__class__.elements=self.OCMSMAYAET.parse(_root)


    def initial(self):
        self.root=ET.Element('Root')
        self.root_init=1
        #ET.dump(self.root)
        print('Root initial.')


    def versionInitial(self,mode=0):
        self._comp_name=''
        if self.root_init==1:
            if mode>=0 and mode<=1:
                data_source=ET.Element('DataSource')
                self.root.append(data_source)
                if mode==0:
                    data_source.attrib={'ProductType':'OCMS','Version':'2021.02.02'}
                    self._comp_name='ComponentV2'
                elif Mode==1:
                    data_source.attrib={'ProductType':'OCMS2_0','Version':'2023.02.16','Source':'Unity'}
                    self._comp_name='Component'
                self.version_init=1
                ET.dump(self.root)
                print('Version initial.')
            else:
                cmds.warning('The mode of number is out of setting.\n')
        else:
            cmds.warning('The root of XML tree is not initial yet.\n')



    def et_initial(self,mode=0):
        self.initial()
        self.versionInitial(mode)
        if self.root_init==1 and self.version_init==1:
            print('Total of elements:' + str(len(self.elements)))
            self.gather_elements_tree(self.elements)
        else:
            cmds.warning('The root and Version are not initial yet.\n')


    def gather_elements_tree(self,elements):
        dict={}
        int=len(elements)
        if isinstance(elements, list):
            dict=self._gather_elements(elements)
            for elem in elements:
                _p_name=self.OCMSMAYAET.parentNode(elem)
                _element=dict[elem]
                if _p_name is None:
                    self.root.append(_element)
                else:
                    P_elem=dict[_p_name]
                    P_elem.append(_element)
            print('Gather '+ str(int) +' elements done.')


    def _gather_elements(self,elements):
        dict={}
        int=len(elements)
        if isinstance(elements, list):
            for elem in elements:
                dict[elem]=self.create_element(elem)
        else:
            print('Elements must be type of list.')
        return dict


    def insert_element(self,target,element):
        target_index=self.root.index(target)
        self.root.insert(target_index,element)
        return target_index


    def create_element(self,element):
        if cmds.objExists(element):
            element=self.__element_tree(element)
        else:
            raise NameError
        return element


    def __element_tree(self,element):
        __EAttr={}
        __EAttr=self.OCMSMAYAET.GetAttributes(element)
        if __EAttr.has_key('Object'):
            __element=ET.Element('Object',__EAttr['Object'])
            if __EAttr.has_key('Transform'):
                elem_t=self.__transform_element(__EAttr['Transform'])
                __element.append(elem_t)
            if __EAttr.has_key('Component'):
                comp_dict=__EAttr['Component']
                for key,value in comp_dict.items():
                    _comp=self.__create_component(key,value)
                    __element.append(_comp)
        return __element


    def __transform_element(self,transform):
        element=ET.Element('Transform')
        if transform.has_key('position'):
            ET.SubElement(element,'position',transform['position'])
        if transform.has_key('rotation'):
            ET.SubElement(element,'rotation',transform['rotation'])
        if transform.has_key('scale'):
            ET.SubElement(element,'scale',transform['scale'])
        return element


    def __create_component(self,name,dict):
        component=self.__component_element(name)
        for key,value in dict.items():
            property=self.__property_element(key,value)
            component.append(property)
        return component


    def __component_element(self,name):
        if self._comp_name == 'ComponentV2':
            component=ET.Element(self._comp_name,{'name':name})
        elif self._comp_name == 'Component':
            component=ET.Element(self._comp_name)
            component.attrib={'name':name,'assembly':'Nadi.OCMS'}
        return component


    def __property_element(self,key,value):
        Property=ET.Element('property')
        Property.set('name',key)
        Property.text=value
        return Property


    def __tostring(self,tree):
        XML_string=''
        XML_string=ET.tostring(tree)
        print('tostring done.')
        return XML_string


    def __prettyxml(self,_tostring):
        DOM_string=DOM.parseString(_tostring)
        XML_string=DOM_string.toprettyxml(indent="\t",encoding='utf-8')
        self.root=ET.fromstring(XML_string)
        self.root.attrib=self.root_attr
        self.XML_TREE=ET.ElementTree(self.root)
        print('pretty xml done.')


    def writxml(self,mode,_file):
        if os.path.exists(_file):
            self.et_initial(mode)
            XML_string=self.__tostring(self.root)
            self.__prettyxml(XML_string)
            self.XML_TREE.write(_file, encoding="utf-8")
            #ET.dump(self.XML_TREE)
            print('xml file writting done.')
        else:
            cmds.warning( 'Some thing wrong with the file path.\n')


        #-------------------------------------------------------------------------------------------------------------------------------
def OCMSMAYAWritXML(_ver_int,_root,_file):
    OCMSMAYAET=OCMSMAYAElement()
    OCMSMAYAETW=OCMSMAYAETWrite(_root)
    OCMSMAYAETW.writxml(_ver_int,_file)
#-------------------------------------------------------------------------------------------------------------------------------
OCMSMAYAWritXML(0,'KSP','E:/NADI_OCMS_XML_Dev_Project/xml/example05.xml')