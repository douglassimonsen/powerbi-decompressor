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


namespace HelloWorld{
  class Program {
    static async Task Open(){
      DependencyInjectionService dependencyInjectionService = DependencyInjectionService.Get();

      IPowerBIConstants powerBIConstants = (IPowerBIConstants) dependencyInjectionService.Resolve<PowerBIConstants>();
      dependencyInjectionService.RegisterInstance<IPowerBIConstants>(powerBIConstants);
      dependencyInjectionService.RegisterType<ISystemEnvironment, SystemEnvironment>();

      IPowerBIConstants powerBIConstants = (IPowerBIConstants) dependencyInjectionService.Resolve<PowerBIConstants>();

      IPowerBISettings powerBISettings;
      StartupConfiguration.StartupConfiguration.SetupEnvironment();
      StartupConfiguration.StartupConfiguration.TryLoadPowerBISettings(dependencyInjectionService.Resolve<ISystemEnvironment>(), out powerBISettings);
      Console.Write(powerBISettings);
      return;
      dependencyInjectionService.RegisterInstance<IPowerBISettings>(powerBISettings);

      dependencyInjectionService.RegisterType<IFeatureSwitchManager, FeatureSwitchManager>().RegisterType<IVersionInfo, VersionInfo>();
      IFeatureSwitchManager featureSwitchManager1 = dependencyInjectionService.Resolve<IFeatureSwitchManager>();
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
      GetLabelFromStreamResult fromStreamResult = await fileInformationProtectionManager.SignInAndDecryptStreamAsync(streamToOpen, null);
      Console.WriteLine("Hello World!");
    }
    static void Main(string[] args){
       Task.Run(Open).Wait();
    }
  }
}