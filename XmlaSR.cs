// Decompiled with JetBrains decompiler
// Type: Microsoft.AnalysisServices.AdomdClient.XmlaSR
// Assembly: Microsoft.PowerBI.AdomdClient, Version=15.0.0.0, Culture=neutral, PublicKeyToken=89845dcd8080cc91
// MVID: F43CE853-F0F3-464F-BA39-D630D391E412
// Assembly location: C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.AdomdClient.dll

using System.Globalization;
using System.Runtime.CompilerServices;

namespace Microsoft.AnalysisServices.AdomdClient
{  
  internal class DummyKeys {
    public static string GetString(){return "dummy";} 
    public static string GetString(params string[] strs){return "dummy";}
  }
  internal class XmlaSR
  {
    public static int dummy;
    protected XmlaSR()
    {
    }

    public static CultureInfo Culture
    {
      get => (CultureInfo) null;
      set => dummy = 0;
    }

    public static string AlreadyConnected => "dummy";

    public static string NotConnected => "dummy";

    public static string CannotConnect => "dummy";

    public static string CannotConnectToRedirector => "dummy";

    public static string ConnectionBroken => "dummy";

    public static string Reconnect_ConnectionInfoIsMissing => "dummy";

    public static string Reconnect_SessionIDIsMissing => "dummy";

    public static string ServerDidNotProvideErrorInfo => "dummy";

    public static string ConnectionCannotBeUsedWhileXmlReaderOpened => "dummy";

    public static string Connect_RedirectorDidntReturnDatabaseInfo => "dummy";

    public static string Connection_WorkbookIsOutdated => "dummy";

    public static string Connection_AnalysisServicesInstanceWasMoved => "dummy";

    public static string Auth_InteractiveLoginRequired => "dummy";

    public static string Auth_MFARequiredAndSupported => "dummy";

    public static string Auth_AcquireTokenFailure => "dummy";

    public static string NetCore_NotSupportedFeature => "dummy";

    public static string NetCore_WindowsOnlySupportedFeature => "dummy";

    public static string NetCore_WindowsDesktopOnlySupportedFeature => "dummy";

    public static string FailedToResolveCluster => "dummy";

    public static string DeprecatedAndNotSupportedFeature => "dummy";

    public static string SoapFormatter_ResponseIsNotRowset => "dummy";

    public static string SoapFormatter_ResponseIsNotDataset => "dummy";

    public static string Cancel_SessionIDNotSpecified => "dummy";

    public static string ConnectionString_Invalid => "dummy";

    public static string ConnectionString_DataSourceNotSpecified => "dummy";

    public static string ConnectionString_MissingIdentityProviderForIntegratedSecurityFederated => "dummy";

    public static string ConnectionString_InvalidIdentityProviderForIntegratedSecurityFederated => "dummy";

    public static string ConnectionString_DataSourceTypeDoesntSupportQuery => "dummy";

    public static string ConnectionString_LinkFileInvalidServer => "dummy";

    public static string ConnectionString_LinkFileMissingServer => "dummy";

    public static string ConnectionString_LinkFileDupEffectiveUsername => "dummy";

    public static string ConnectionString_LinkFileCannotRevert => "dummy";

    public static string ConnectionString_LinkFileCannotDelegate => "dummy";

    public static string ConnectionString_MissingPassword => "dummy";

    public static string ConnectionString_AsAzure_DataSourcePathMoreThanOneSegment => "dummy";

    public static string ConnectionString_PbiDedicated_MissingInitialCatalog => "dummy";

    public static string ConnectionString_PbiDedicated_MissingRestrictCatalog => "dummy";

    public static string ConnectionString_AsAzure_SspiAndUseAdalCacheTogetherNotSupported => "dummy";

    public static string ConnectionString_PbiDedicated_WrongIntendedUsage => "dummy";

    public static string ConnectionString_Untrusted_Endpoint => "dummy";

    public static string UnknownServerResponseFormat => nameof (UnknownServerResponseFormat);

    public static string AfterExceptionAllTagsShouldCloseUntilMessagesSection => "dummy";

    public static string ErrorCodeIsMissingFromRowsetError => "dummy";

    public static string ErrorCodeIsMissingFromDatasetError => "dummy";

    public static string ExceptionRequiresXmlaErrorsInMessagesSection => "dummy";

    public static string MessagesSectionIsEmpty => "dummy";

    public static string EmptyRootIsNotEmpty => "dummy";

    public static string Resultset_IsNotRowset => "dummy";

    public static string DataReaderClosedError => "dummy";

    public static string DataReaderInvalidRowError => "dummy";

    public static string NonSequentialColumnAccessError => "dummy";

    public static string DataReader_IndexOutOfRange => "dummy";

    public static string Authentication_Failed => "dummy";

    public static string Authentication_Sspi_SchannelCantDelegate => "dummy";

    public static string Authentication_Sspi_SchannelSupportsOnlyPrivacyLevel => "dummy";

    public static string Authentication_Sspi_SchannelUnsupportedImpersonationLevel => "dummy";

    public static string Authentication_Sspi_SchannelUnsupportedProtectionLevel => "dummy";

    public static string Authentication_Sspi_SchannelAnonymousAmbiguity => "dummy";

    public static string Authentication_MsoID_MissingSignInAssistant => "dummy";

    public static string Authentication_MsoID_InternalError => "dummy";

    public static string Authentication_MsoID_InvalidCredentials => "dummy";

    public static string Authentication_MsoID_SsoFailed => "dummy";

    public static string Authentication_MsoID_SsoFailedNonDomainUser => "dummy";

    public static string Authentication_ClaimsToken_AuthorityNotFound => "dummy";

    public static string Authentication_ClaimsToken_UserIdAndPasswordRequired => "dummy";

    public static string Authentication_ClaimsToken_IdentityProviderFormatInvalid => "dummy";

    public static string Authentication_AsAzure_OnlySspiOrClaimsTokenSupported => "dummy";

    public static string Authentication_PbiDedicated_OnlyClaimsTokenSupported => "dummy";

    public static string DimeReader_CannotReadFromStream => "dummy";

    public static string DimeReader_IsClosed => "dummy";

    public static string DimeReader_PreviousRecordStreamStillOpened => "dummy";

    public static string DimeRecord_StreamShouldBeReadable => "dummy";

    public static string DimeRecord_StreamShouldBeWriteable => "dummy";

    public static string DimeRecord_InvalidContentLength => "dummy";

    public static string DimeRecord_PropertyOnlyAvailableForReadRecords => "dummy";

    public static string DimeRecord_InvalidChunkSize => "dummy";

    public static string DimeRecord_UnableToReadFromStream => "dummy";

    public static string DimeRecord_StreamIsClosed => "dummy";

    public static string DimeRecord_ReadNotAllowed => "dummy";

    public static string DimeRecord_WriteNotAllowed => "dummy";

    public static string DimeRecord_TypeFormatEnumUnchangedNotAllowed => "dummy";

    public static string DimeRecord_MediaTypeNotDefined => "dummy";

    public static string DimeRecord_NameMustNotBeDefinedForFormatNone => "dummy";

    public static string DimeRecord_EncodedTypeLengthExceeds8191 => "dummy";

    public static string DimeRecord_OffsetAndCountShouldBePositive => "dummy";

    public static string DimeRecord_ContentLengthExceeded => "dummy";

    public static string DimeRecord_OnlySingleRecordMessagesAreSupported => "dummy";

    public static string DimeRecord_DataTypeShouldBeSpecifiedOnTheFirstChunk => "dummy";

    public static string DimeRecord_DataTypeIsOnlyForTheFirstChunk => "dummy";

    public static string DimeRecord_IDIsOnlyForFirstChunk => "dummy";

    public static string DimeWriter_CannotWriteToStream => "dummy";

    public static string DimeWriter_WriterIsClosed => "dummy";

    public static string DimeWriter_InvalidDefaultChunkSize => "dummy";

    public static string TcpStream_MaxSignatureExceedsProtocolLimit => "dummy";

    public static string IXMLAInterop_OnlyZeroOffsetIsSupported => "dummy";

    public static string IXMLAInterop_StreamDoesNotSupportReverting => "dummy";

    public static string IXMLAInterop_StreamDoesNotSupportLocking => "dummy";

    public static string IXMLAInterop_StreamDoesNotSupportUnlocking => "dummy";

    public static string IXMLAInterop_StreamCannotBeCloned => "dummy";

    public static string XmlaClient_StartRequest_ThereIsAnotherPendingRequest => "dummy";

    public static string XmlaClient_StartRequest_ThereIsAnotherPendingResponse => "dummy";

    public static string XmlaClient_SendRequest_RequestStreamCannotBeRead => "dummy";

    public static string XmlaClient_SendRequest_NoRequestWasCreated => "dummy";

    public static string XmlaClient_ConnectTimedOut => "dummy";

    public static string XmlaClient_SendRequest_ThereIsAnotherPendingResponse => "dummy";

    public static string XmlaClient_CannotConnectToLocalCubeWithRestictedClient => "dummy";

    public static string XmlaClient_PbiPublicXmla_DatasetNotSpecified => "dummy";

    public static string XmlaClient_PbiPublicXmlaWithEmbedToken_ToPBIShared_NotSupported => "dummy";

    public static string XmlaClient_PbiPublicXmlaWithEmbedToken_UserId_Prop_NotSupported => "dummy";

    public static string XmlaClient_PbiPublicXmlaWithEmbedToken_Missing_InitialCatalog => "dummy";

    public static string Decompression_InitializationFailed => "dummy";

    public static string Compression_InitializationFailed => "dummy";

    public static string InvalidArgument => "dummy";

    public static string ProvidePath => "dummy";

    public static string InternalError => "dummy";

    public static string InternalErrorAndInvalidBufferType => "dummy";

    public static string LocalCube_FileNotOpened(string cubeFile) => "dummy";

    public static string Instance_NotFound(string instance, string server) => "dummy";

    public static string UnexpectedXsiType(string type) => "dummy";

    public static string ConnectionString_InvalidPropertyNameFormat(string propertyName) => "dummy";

    public static string ConnectionString_UnsupportedPropertyValue(
      string propertyName,
      string value)
    {
      // ISSUE: reference to a compiler-generated method
      return "dummy";
    }

    public static string ConnectionString_OpenedQuoteIsNotClosed(char openQuoteChar, int index) => "dummy";

    public static string ConnectionString_ExpectedSemicolonNotFound(int index) => "dummy";

    public static string ConnectionString_ExpectedEqualSignNotFound(int fromIndex) => "dummy";

    public static string ConnectionString_InvalidCharInPropertyName(char invalidChar, int index) => "dummy";

    public static string ConnectionString_InvalidCharInUnquotedPropertyValue(
      char invalidChar,
      int index)
    {
      // ISSUE: reference to a compiler-generated method
      return "dummy";
    }

    public static string ConnectionString_PropertyNameNotDefined(int equalIndex) => "dummy";

    public static string ConnectionString_InvalidIntegratedSecurityForNative(
      string integratedSecurity)
    {
      // ISSUE: reference to a compiler-generated method
      return "dummy";
    }

    public static string ConnectionString_InvalidProtectionLevelForHttp(string protectionLevel) => "dummy";

    public static string ConnectionString_InvalidProtectionLevelForHttps(string protectionLevel) => "dummy";

    public static string ConnectionString_InvalidImpersonationLevelForHttp(string impersonationLevel) => "dummy";

    public static string ConnectionString_InvalidImpersonationLevelForHttps(
      string impersonationLevel)
    {
      // ISSUE: reference to a compiler-generated method
      return "dummy";
    }

    public static string ConnectionString_InvalidIntegratedSecurityForHttpOrHttps(
      string integratedSecurity)
    {
      // ISSUE: reference to a compiler-generated method
      return "dummy";
    }

    public static string ConnectionString_PropertyNotApplicableWithTheDataSourceType(
      string propertyName)
    {
      // ISSUE: reference to a compiler-generated method
      return "dummy";
    }

    public static string ConnectionString_LinkFileParseError(int size) => "dummy";

    public static string ConnectionString_LinkFileDownloadError(string linkFileName) => "dummy";

    public static string ConnectionString_ExternalConnectionIsIncomplete(string missingPropertyName) => "dummy";

    public static string ConnectionString_ASAzure_FetchLinkReferenceFailed(string linkFileUri) => "dummy";

    public static string ConnectionString_ASAzure_InvalidLinkReferenceUri(string linkFileUri) => "dummy";

    public static string ConnectionString_ASAzure_InvalidLinkReferenceCustomPort(string linkFileUri) => "dummy";

    public static string ConnectionString_PbiDataset_Missing_Metadata(string missingParam) => "dummy";

    public static string ConnectionString_ShilohIsNoLongerSupported(string propertyName) => "dummy";

    public static string UnrecognizedElementInMessagesSection(string elementName) => "dummy";

    public static string UnexpectedElement(string elementName, string namespaceName) => "dummy";

    public static string MissingElement(string elementName, string namespaceName) => "dummy";

    public static string Authentication_Sspi_PackageNotFound(string packageName) => "dummy";

    public static string Authentication_Sspi_PackageDoesntSupportCapability(
      string package,
      string capability)
    {
      // ISSUE: reference to a compiler-generated method
      return "dummy";
    }

    public static string Authentication_Sspi_FlagNotEstablished(string flagName) => "dummy";

    public static string Authentication_ClaimsToken_AdalLoadingError(string component) => "dummy";

    public static string Authentication_ClaimsToken_AdalError(string message) => "dummy";

    public static string DimeRecord_InvalidUriFormat(string uri) => "dummy";

    public static string DimeRecord_VersionNotSupported(int version) => "dummy";

    public static string DimeRecord_TypeFormatShouldBeMedia(string value) => "dummy";

    public static string DimeRecord_TypeFormatShouldBeUnchanged(string value) => "dummy";

    public static string DimeRecord_ReservedFlagShouldBeZero(byte value) => "dummy";

    public static string DimeRecord_DataTypeNotSupported(string value) => "dummy";

    public static string DimeRecord_InvalidHeaderFlags(int begin, int end, int chunked) => "dummy";

    public static string Dime_DataTypeNotSupported(string value) => "dummy";

    public static string XmlaClient_PbiPublicXmla_InvalidDataSourceUriFormat(string uri) => "dummy";

    public static string XmlaClient_PbiPremium_WorkspaceNotFound(string technicalDetails) => "dummy";

    public static string XmlaClient_PbiPremium_WorkspaceNotOnPremium(string technicalDetails) => "dummy";

    public static string XmlaClient_PbiPremium_WorkspaceNameDuplicated(string technicalDetails) => "dummy";

    public static string XmlaClient_PbiPublicXmla_DatasetNotFound(
      string datasetFriendlyName,
      string technicalDetails)
    {
      // ISSUE: reference to a compiler-generated method
      return "dummy";
    }

    public static string XmlaClient_PbiPublicXmla_DatasetNameDuplicated(
      string datasetFriendlyName,
      string technicalDetails)
    {
      // ISSUE: reference to a compiler-generated method
      return "dummy";
    }

    public static string Decompression_Failed(
      int compressedSize,
      int expectedDecompressedSize,
      int actualDecompressedSize)
    {
      // ISSUE: reference to a compiler-generated method
      return "dummy";
    }

    public static string UnsupportedDataFormat(string format) => "dummy";

    public static string UnsupportedMethod(string name) => "dummy";

    public static string DirectoryNotFound(string path) => "dummy";

    public static string HttpStream_ASAzure_TechnicalDetailsText(
      string rootActivityId,
      string currentUtcDate)
    {
      // ISSUE: reference to a compiler-generated method
      return "dummy";
    }

    public static string HttpStream_PbiShared_TechnicalDetailsText(string rootActivityId) => "dummy";
  }
}
