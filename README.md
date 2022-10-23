// Assembly location: C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.AdomdClient.dll

C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.Client.Windows.dll
Report Factory, lines 479-480

C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.Client.Windows.dll
Load To Database From PBix, line 21


XMLA sent
"C:\Users\mwham\AppData\Local\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces\AnalysisServicesWorkspace_8d363818-c720-4e18-89c1-294fc2027b96\Data\FlightRecorderCurrent.trc"

Update Tables
<Batch Transaction="false" xmlns="http://schemas.microsoft.com/analysisservices/2003/engine">
  <Delete xmlns="http://schemas.microsoft.com/analysisservices/2014/engine">
    <DatabaseID>15dfc18a-0908-493c-8f21-8162ba250dab</DatabaseID>
    <Annotations>
      <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:sql="urn:schemas-microsoft-com:xml-sql">
        <xs:element>
          <xs:complexType>
            <xs:sequence>
              <xs:element type="row"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:complexType name="row">
          <xs:sequence>
            <xs:element name="ID" type="xs:unsignedLong" sql:field="ID" minOccurs="0"/>
          </xs:sequence>
        </xs:complexType>
      </xs:schema>
      <row xmlns="urn:schemas-microsoft-com:xml-analysis:rowset">
        <ID>879</ID>
      </row>
    </Annotations>
  </Delete>
  <Refresh xmlns="http://schemas.microsoft.com/analysisservices/2014/engine">
    <DatabaseID>15dfc18a-0908-493c-8f21-8162ba250dab</DatabaseID>
    <Tables>
      <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:sql="urn:schemas-microsoft-com:xml-sql">
        <xs:element>
          <xs:complexType>
            <xs:sequence>
              <xs:element type="row"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:complexType name="row">
          <xs:sequence>
            <xs:element name="ID" type="xs:unsignedLong" sql:field="ID" minOccurs="0"/>
            <xs:element name="ID.Table" type="xs:string" sql:field="ID.Table" minOccurs="0"/>
            <xs:element name="RefreshType" type="xs:long" sql:field="RefreshType" minOccurs="0"/>
          </xs:sequence>
        </xs:complexType>
      </xs:schema>
      <row xmlns="urn:schemas-microsoft-com:xml-analysis:rowset">
        <ID>789</ID>
        <RefreshType>4</RefreshType>
      </row>
    </Tables>
    <Model>
      <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:sql="urn:schemas-microsoft-com:xml-sql">
        <xs:element>
          <xs:complexType>
            <xs:sequence>
              <xs:element type="row"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:complexType name="row">
          <xs:sequence>
            <xs:element name="RefreshType" type="xs:long" sql:field="RefreshType" minOccurs="0"/>
          </xs:sequence>
        </xs:complexType>
      </xs:schema>
      <row xmlns="urn:schemas-microsoft-com:xml-analysis:rowset">
        <RefreshType>3</RefreshType>
      </row>
    </Model>
  </Refresh>
  <SequencePoint xmlns="http://schemas.microsoft.com/analysisservices/2014/engine">
    <DatabaseID>15dfc18a-0908-493c-8f21-8162ba250dab</DatabaseID>
  </SequencePoint>
</Batch>