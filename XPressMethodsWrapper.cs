// Decompiled with JetBrains decompiler
// Type: Microsoft.AnalysisServices.AdomdClient.XpressMethodsWrapper
// Assembly: Microsoft.PowerBI.AdomdClient, Version=15.0.0.0, Culture=neutral, PublicKeyToken=89845dcd8080cc91
// MVID: F43CE853-F0F3-464F-BA39-D630D391E412
// Assembly location: C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.AdomdClient.dll

using System;
using System.ComponentModel;
using System.IO;
using System.Reflection;
using System.Runtime.InteropServices;

namespace Microsoft.AnalysisServices.AdomdClient
{
  internal sealed class XpressMethodsWrapper : LibraryHandle
  {
    private XpressMethodsWrapper.CompressInitDelegate compressInitDelegate;
    private XpressMethodsWrapper.CompressDelegate compressDelegate;
    private XpressMethodsWrapper.CompressCloseDelegate compressCloseDelegate;
    private XpressMethodsWrapper.DecompressInitDelegate decompressInitDelegate;
    private XpressMethodsWrapper.DecompressDelegate decompressDelegate;
    private XpressMethodsWrapper.DecompressCloseDelegate decompressCloseDelegate;
    private static XpressMethodsWrapper xpressMethodsWrapper = (XpressMethodsWrapper) null;
    private static XpressMethodsWrapper.Lock LockForCreatingWrapper = new XpressMethodsWrapper.Lock();
    private static readonly string XpressPath = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location) + "\\msasxpress.dll";
    internal static readonly bool XpressAvailable;
    internal const int MaxBlock = 65536;

    static XpressMethodsWrapper(){
      if (!File.Exists(XpressMethodsWrapper.XpressPath))
        XpressMethodsWrapper.XpressPath = Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles) + "\\Microsoft SQL Server\\150\\shared\\msasxpress.dll";
      XpressMethodsWrapper.XpressAvailable = File.Exists(XpressMethodsWrapper.XpressPath);
    }

    internal static XpressMethodsWrapper XpressWrapper
    {
      get
      {
        lock (XpressMethodsWrapper.LockForCreatingWrapper)
        {
          if (XpressMethodsWrapper.xpressMethodsWrapper == null || XpressMethodsWrapper.xpressMethodsWrapper.IsInvalid)
          {
            XpressMethodsWrapper.xpressMethodsWrapper = XpressMethodsWrapper.LoadLibrary(XpressMethodsWrapper.XpressPath);
            XpressMethodsWrapper.xpressMethodsWrapper.SetDelegates();
          }
          return XpressMethodsWrapper.xpressMethodsWrapper;
        }
      }
    }

    private XpressMethodsWrapper(){}

    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true, BestFitMapping = false)]
    private static extern XpressMethodsWrapper LoadLibrary([MarshalAs(UnmanagedType.LPTStr), In] string fileName);

    private void SetDelegates()
    {
      this.compressInitDelegate = (XpressMethodsWrapper.CompressInitDelegate) XpressMethodsWrapper.xpressMethodsWrapper.GetDelegate("CompressInit", typeof (XpressMethodsWrapper.CompressInitDelegate));
      this.compressDelegate = (XpressMethodsWrapper.CompressDelegate) XpressMethodsWrapper.xpressMethodsWrapper.GetDelegate("Compress", typeof (XpressMethodsWrapper.CompressDelegate));
      this.compressCloseDelegate = (XpressMethodsWrapper.CompressCloseDelegate) XpressMethodsWrapper.xpressMethodsWrapper.GetDelegate("CompressClose", typeof (XpressMethodsWrapper.CompressCloseDelegate));
      this.decompressInitDelegate = (XpressMethodsWrapper.DecompressInitDelegate) XpressMethodsWrapper.xpressMethodsWrapper.GetDelegate("DecompressInit", typeof (XpressMethodsWrapper.DecompressInitDelegate));
      this.decompressDelegate = (XpressMethodsWrapper.DecompressDelegate) XpressMethodsWrapper.xpressMethodsWrapper.GetDelegate("Decompress", typeof (XpressMethodsWrapper.DecompressDelegate));
      this.decompressCloseDelegate = (XpressMethodsWrapper.DecompressCloseDelegate) XpressMethodsWrapper.xpressMethodsWrapper.GetDelegate("DecompressClose", typeof (XpressMethodsWrapper.DecompressCloseDelegate));
    }

    internal IntPtr CompressInit(int maxInputSize, int compressionLevel) => this.CheckEmptyHandle(this.compressInitDelegate(maxInputSize, compressionLevel));

    internal int Compress(
      IntPtr compressHandle,
      byte[] input,
      int inputOffset,
      int inputSize,
      byte[] output,
      int outputOffset,
      int outputSize){
      return this.compressDelegate(compressHandle, input, inputOffset, inputSize, output, outputOffset, outputSize);
    }

    internal void CompressClose(IntPtr compressHandle) => this.compressCloseDelegate(compressHandle);

    internal IntPtr DecompressInit() => this.CheckEmptyHandle(this.decompressInitDelegate());

    internal int Decompress(
      IntPtr decompressHandle,
      byte[] input,
      int inputSize,
      byte[] output,
      int outputSize,
      int bytesToDecompress){
      return this.decompressDelegate(decompressHandle, input, inputSize, output, outputSize, bytesToDecompress);
    }

    internal void DecompressClose(IntPtr decompressHandle) => this.decompressCloseDelegate(decompressHandle);

    private class Lock{}

    private delegate IntPtr CompressInitDelegate([In] int maxInputSize, [In] int compressionLevel);

    private delegate int CompressDelegate(
      [In] IntPtr compressHandle,
      [MarshalAs(UnmanagedType.LPArray), In] byte[] input,
      [In] int inputOffset,
      [In] int inputSize,
      [MarshalAs(UnmanagedType.LPArray), In] byte[] output,
      [In] int outputOffset,
      [In] int outputSize);

    private delegate void CompressCloseDelegate([In] IntPtr compressHandle);

    private delegate IntPtr DecompressInitDelegate();

    private delegate int DecompressDelegate(
      [In] IntPtr decompressHandle,
      [MarshalAs(UnmanagedType.LPArray), In] byte[] input,
      [In] int inputSize,
      [MarshalAs(UnmanagedType.LPArray), In] byte[] output,
      [In] int outputSize,
      [In] int bytesToDecompress);

    private delegate void DecompressCloseDelegate([In] IntPtr decompressHandle);
  }
}
