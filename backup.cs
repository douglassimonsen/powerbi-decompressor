using Microsoft.Mashup.Client.UI.Shared;
using Microsoft.Mashup.Client.UI.Shared.HtmlControls.Results.Binary;
using Microsoft.Mashup.Client.UI.Shared.Models;
using Microsoft.Mashup.Client.UI.Shared.PluggableProtocol;
using Microsoft.Mashup.Client.UI.Shared.Themes;
using Microsoft.Mashup.Client.UI.Shared.Ux;
using Microsoft.Mashup.Client.UI.Shared.Ux.FloatingDialog.SimpleDialog;
using Microsoft.Mashup.Client.UI.Shared.WebTableLearning;
using Microsoft.Mashup.Client.UI.WebViews.Windows;
using Microsoft.Mashup.Client.UI.Windows;
using Microsoft.Mashup.DocumentServices;
using Microsoft.Mashup.DocumentServices.Names;
using Microsoft.Mashup.DocumentServices.Strings;
using Microsoft.Mashup.Host.Document;
using Microsoft.Mashup.Host.Document.Evaluation;
using Microsoft.Mashup.Host.Document.Evaluation.Services;
using Microsoft.Mashup.Host.Document.Formulas;
using Microsoft.Mashup.Host.Document.Storage;
using Microsoft.PowerBI.Client.Shared;
using Microsoft.PowerBI.Client.Telemetry;
using Microsoft.PowerBI.Client.Windows;
using Microsoft.PowerBI.Client.Windows.AnalysisServices;
using Microsoft.PowerBI.Client.Windows.AnalysisServices.DataTypeFormat;
using Microsoft.PowerBI.Client.Windows.AnalysisServices.Relationships;
using Microsoft.PowerBI.Client.Windows.Commands.ApplicationCommands;
using Microsoft.PowerBI.Client.Windows.Configs;
using Microsoft.PowerBI.Client.Windows.Diagnostics;
using Microsoft.PowerBI.Client.Windows.DiagramView;
using Microsoft.PowerBI.Client.Windows.Eim.InformationProtection;
using Microsoft.PowerBI.Client.Windows.Eim.InformationProtection.Mip;
using Microsoft.PowerBI.Client.Windows.Events;
using Microsoft.PowerBI.Client.Windows.ExploreHost;
using Microsoft.PowerBI.Client.Windows.LiveConnectHelpers.AnalysisServices;
using Microsoft.PowerBI.Client.Windows.MashupConector;
using Microsoft.PowerBI.Client.Windows.Modeling;
using Microsoft.PowerBI.Client.Windows.Modeling.Hosting;
using Microsoft.PowerBI.Client.Windows.PowerBIService;
using Microsoft.PowerBI.Client.Windows.Printing;
using Microsoft.PowerBI.Client.Windows.Python;
using Microsoft.PowerBI.Client.Windows.QueryFolding;
using Microsoft.PowerBI.Client.Windows.R;
using Microsoft.PowerBI.Client.Windows.Services;
using Microsoft.PowerBI.Client.Windows.SSRSService;
using Microsoft.PowerBI.Client.Windows.Storage;
using Microsoft.PowerBI.Client.Windows.Telemetry;
using Microsoft.PowerBI.Client.Windows.Themes;
using Microsoft.PowerBI.Client.Windows.WebTableLearning;
using Microsoft.PowerBI.Common;
using Microsoft.PowerBI.DiagramView.Diagram;
using Microsoft.PowerBI.ExploreHost;
using Microsoft.PowerBI.ExploreHost.Lucia;
using Microsoft.PowerBI.ExploreHost.SemanticQuery;
using Microsoft.PowerBI.ExploreServiceCommon.Interfaces;
using Microsoft.PowerBI.Lucia;
using Microsoft.PowerBI.Modeling.Contracts;
using Microsoft.PowerBI.Modeling.Contracts.Hosting;
using Microsoft.PowerBI.Modeling.Contracts.MashupQuery;
using Microsoft.PowerBI.Modeling.Engine.InternalContracts;
using Microsoft.PowerBI.Modeling.Engine.Loader;
using Microsoft.PowerBI.ReportingServicesHost;
using Microsoft.PowerBI.Telemetry;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using StartupConfiguration;


namespace HelloWorld2 {
  class Program {
    static void Open(){
      Stream streamToOpen = (Stream) File.Open("api.pbix", FileMode.Open);
      Console.WriteLine("Hello World!");    
    }
     static void Mai2n(){
      
      DependencyInjectionService dependencyInjectionService = DependencyInjectionService.Get();      
      dependencyInjectionService.RegisterType<IFileManager, FileManager>()
                                .RegisterType<IEventAggregationService, EventAggregationService>();
      IPowerBIConstants powerBIConstants = (IPowerBIConstants) dependencyInjectionService.Resolve<PowerBIConstants>();

      IPowerBISettings powerBISettings;
      StartupConfiguration.StartupConfiguration.SetupEnvironment();
      StartupConfiguration.StartupConfiguration.TryLoadPowerBISettings(dependencyInjectionService.Resolve<ISystemEnvironment>(), out powerBISettings);


      IOAuthDialogFactory oauthDialogFactory = ApplicationOptions.DisableEdgeChromiumOAuth ? (IOAuthDialogFactory) null : (IOAuthDialogFactory) new ModernBrowserOAuthDialogFactory(powerBISettings.LocalDataPath, ApplicationOptions.ExtendEdgeChromiumOAuthAllowList, ApplicationOptions.EdgeChromiumOAuthAllowListAll, ApplicationOptions.ExtendSystemBrowserOAuthAllowList, ApplicationOptions.DisableSystemBrowserOAuth);
      ITelemetryManager powerBITelemetryManager = (ITelemetryManager) null;
      IThemeServices themeServices = (IThemeServices) null;

      using (IUIHost uiHost1 = UIHost.Initialize(
        (IApplicationConstants) powerBIConstants, 
        (IApplicationSettings) powerBISettings, 
        (IPluggableProtocolSettings) new PowerBIPluggableProtocolSettings(), 
        (IUserFeedbackServices) new PowerBIUserFeedbackServices(
          powerBITelemetryManager, 
          dependencyInjectionService.Resolve<IPowerBIWindowServiceFactory>(), 
          dependencyInjectionService.Resolve<IWindowsErrorReportingService>(), 
          powerBISettings.AdditionalFeedbackParameters, 
          dependencyInjectionService.Resolve<ISystemEnvironment>()), 
          themeServices, 
          (IStringProvider) dependencyInjectionService.Resolve<IPowerBIStringProvider>(), 
          (IFontProvider) new FontProvider(), 
          (IComponentFactories) new PowerBIWin32ComponentFactories(oauthDialogFactory), 
          (IChallengeResolverFactories) new ChallengeResolverFactories(), 
          (Func<SynchronizationContext, IExceptionFilter>) (synchronizationContext => (IExceptionFilter) DefaultExceptionFilter.Instance)
        )){
        dependencyInjectionService.RegisterInstance<IUIHost>(uiHost1)
                                  .RegisterInstance<SynchronizationContext>(uiHost1.UIThreadContext)
                                  //.RegisterType<IAnalysisServicesLoadContextFactory, AnalysisServicesLoadContextFactory>()
                                  .RegisterType<IBinaryResultContextMenuProvider, BinaryResultContextMenuProvider>()
                                  //.RegisterType<IExceptionHandler, PowerBIUnexpectedExceptionHandler>()
                                  .RegisterType<IFeatureSettings, FeatureSettings>()
                                  .RegisterType<IFeatureSwitchManager, FeatureSwitchManager>()
                                  .RegisterType<IHttpService, HttpService>()
                                  .RegisterType<IEventAggregationService, EventAggregationService>()
                                  .RegisterType<IViewSelectionService, ViewSelectionService>()
                                  .RegisterType<ISchemaChangeApplierFactory, SchemaChangeApplierFactory>()
                                  .RegisterType<IPowerQueryToModelLoader, PowerQueryToModelLoader>()
                                  .RegisterType<IQueryStorageModeResolver, QueryStorageModeResolver>()
                                  .RegisterType<IRelationshipManager, RelationshipManager>(DependencyInjectionService.IsolationModel.Transient)
                                  .RegisterType<IModelAuthoringRoutingService, ModelAuthoringRoutingService>()
                                  .RegisterType<IModelExtensionService, ModelExtensionService>()
                                  .RegisterType<IUIBlockingService, UIBlockingService>()
                                  .RegisterType<IPowerBIPackagingService, PowerBIPackagingService>()
                                  .RegisterType<IFileManager, FileManager>()
                                  .RegisterType<IDiagramLayoutService, DiagramLayoutService>()
                                  .RegisterType<ITypeNameProvider, TypeNameProvider>()
                                  //.RegisterType<IContextMenuFormulaAreaProvider, ContextMenuFormulaAreaProvider>()
                                  //.RegisterType<ICefBrowserFactory, CefBrowserFactory>()
                                  //.RegisterInstance<IFileHistoryManager>(fileHistoryManager)
                                  //.RegisterInstance<IUpdateNotificationServices>((IUpdateNotificationServices) notificationService)
                                  .RegisterType<IUpdateNotificationManager, UpdateNotificationManager>()
                                  .RegisterType<IFileDialogManager, Win32FileDialogManager>()
                                  .RegisterType<FormulaHistoryManager, FormulaHistoryManager>()
                                  .RegisterType<IWarningNotificationService, WarningNotificationService>()
                                  .RegisterType<IWarningDetectionService, WarningDetectionService>()
                                  .RegisterType<IFileOperationUIHandler, FileOperationUIHandler>()
                                  .RegisterType<IVersionInfo, VersionInfo>()
                                  .RegisterType<IAdomdConnectionFactory, AdomdConnectionWrapperFactory>()
                                  .RegisterType<IApplicationCommands, Microsoft.PowerBI.Client.Windows.Commands.ApplicationCommands.ApplicationCommands>()
                                  .RegisterType<IShellExecuteHandler, ShellExecuteHandler>()
                                  //.RegisterType<ILuciaSessionActivationManager, LuciaSessionActivationManager>()
                                  .RegisterType<IFileStreamFactory, FileStreamFactory>()
                                  .RegisterType<IAccessibilityService, AccessibilityService>()
                                  .RegisterType<IMinervaModalDialogManager, MinervaModalDialogManager>()
                                  .RegisterType<IPdfiumService, PdfiumService>()
                                  .RegisterType<ITlsConfiguration, MachineTlsConfiguration>()
                                  //.RegisterType<IFileSystem, FileSystem>()
                                  .RegisterType<IApplicationPropertiesProvider, PowerBIPropertiesProvider>()
                                  .RegisterType<IFoldedArtifactsGenerator, FoldedArtifactsGenerator>()
                                  .RegisterType<IFoldedArtifactsCacheService, FoldedArtifactsCacheService>()
                                  .RegisterType<IModelingQueryServices, ModelingQueryServices>()
                                  .RegisterType<IMashupExpressionAnalyzer, ModelingMashupExpressionAnalyzer>(DependencyInjectionService.IsolationModel.Transient)
                                  .RegisterType<IExternalToolsManager, ExternalToolsManager>()
                                  .RegisterInstance<ITelemetryManager>(powerBITelemetryManager)
                                  //.RegisterType<IOpenSaveUI, LocalFileOpenSaveUI>(DependencyInjectionService.IsolationModel.Transient, "local")
                                  //.RegisterType<IOpenSaveUI, SsrsOpenSaveUI>(DependencyInjectionService.IsolationModel.Transient, "ssrs")
                                  .RegisterType<ICredentialRefreshServiceProvider, CredentialRefreshServiceProvider>();
      Stream streamToOpen = (Stream) File.Open("api.pbix", FileMode.Open);
      FileInformationProtectionManager fileInformationProtectionManager = new FileInformationProtectionManager(
        null,
        null,
        null,
        null,
        null,
        null,
        null
      );
      //GetLabelFromStreamResult fromStreamResult = await fileInformationProtectionManager.SignInAndDecryptStreamAsync(streamToOpen, null);

      }
    }
  }
}