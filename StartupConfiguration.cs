// Decompiled with JetBrains decompiler
// Type: Microsoft.PowerBI.Client.StartupConfiguration
// Assembly: PBIDesktop, Version=1.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35
// MVID: B0DCECC5-26F0-4193-A53D-78769917F02B
// Assembly location: C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe

using Microsoft.Mashup.Client.Packaging;
using Microsoft.Mashup.Host.Document;
using Microsoft.PowerBI.Client.Shared;
using System.Diagnostics;
using System.Net;

namespace StartupConfiguration
{
  public static class StartupConfiguration
  {
    public static void SetupEnvironment()
    {
      StartupConfiguration.ConfigureHttpsProtocolVersions();
      StartupConfiguration.ConfigureConnectionProperties();
      StartupConfiguration.SetWinDir();
      StartupConfiguration.SetProcessDpiAware();
    }

    public static bool TryLoadPowerBISettings(
      ISystemEnvironment systemEnvironment,
      out IPowerBISettings powerBISettings)
    {
      powerBISettings = (IPowerBISettings) null;
      try
      {
        powerBISettings = PowerBISettingsFactory.GetSettingsFromAppConfig(systemEnvironment);
      }
      catch (Exception ex)
      {
        if (!SafeExceptions.IsSafeException(ex))
        {
          throw;
        }
        else
        {
          return false;
        }
      }
      StartupConfiguration.TryMigrateSettings(powerBISettings);
      if (!PackageComponents.IsDelegationSupported())
      {
        return false;
      }
      return true;
    }

    public static void TryMigrateSettings(IPowerBISettings powerBISettings)
    {
      if (powerBISettings.LocalDataPath == powerBISettings.ClassicLocalDataPath)
        return;
      SafeExceptions.TryInvoke((Action) (() =>
      {
        if (Directory.Exists(powerBISettings.LocalDataPath))
          return;
        string str = (string) null;
        if (Directory.Exists(powerBISettings.ClassicLocalDataPath))
          str = powerBISettings.ClassicLocalDataPath;
        else if (Directory.Exists(powerBISettings.OldLocalDataPath))
          str = powerBISettings.OldLocalDataPath;
        if (str == null)
          return;
        Process process = new Process();
        process.StartInfo.FileName = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.System), "robocopy.exe");
        process.StartInfo.Arguments = "/e \"" + str + "\" \"" + powerBISettings.LocalDataPath + "\"";
        process.StartInfo.CreateNoWindow = true;
        process.StartInfo.UseShellExecute = false;
        process.Start();
        process.WaitForExit();
      }));
    }

    private static void ConfigureConnectionProperties()
    {
      ServicePointManager.DefaultConnectionLimit = 24;
      ServicePointManager.SetTcpKeepAlive(true, 180000, 180000);
    }

    private static void ConfigureHttpsProtocolVersions() => ServicePointManager.SecurityProtocol = ServicePointManager.SecurityProtocol & ~SecurityProtocolType.Ssl3 | SecurityProtocolType.Tls | SecurityProtocolType.Tls11 | SecurityProtocolType.Tls12;

    private static void SetWinDir()
    {
      string environmentVariable = Environment.GetEnvironmentVariable("SystemRoot");
      if (string.IsNullOrEmpty(environmentVariable))
        return;
      Environment.SetEnvironmentVariable("WinDir", environmentVariable);
    }

    private static void SetProcessDpiAware()
    {
      try
      {
        //NativeMethods.SetProcessDPIAware();
      }
      catch (Exception ex)
      {
        if (SafeExceptions.IsSafeException(ex))
          return;
        throw;
      }
    }
  }
}
