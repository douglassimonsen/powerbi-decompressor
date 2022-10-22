// Decompiled with JetBrains decompiler
// Type: Microsoft.AnalysisServices.AdomdClient.LibraryHandle
// Assembly: Microsoft.PowerBI.AdomdClient, Version=15.0.0.0, Culture=neutral, PublicKeyToken=89845dcd8080cc91
// MVID: F43CE853-F0F3-464F-BA39-D630D391E412
// Assembly location: C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.AdomdClient.dll

using System;
using System.ComponentModel;
using System.Runtime.InteropServices;
using System.Security;

namespace Microsoft.AnalysisServices.AdomdClient
{
  internal class LibraryHandle : SafeHandle
  {
    protected LibraryHandle()
      : base(IntPtr.Zero, true)
    {
    }

    public override bool IsInvalid => this.handle == IntPtr.Zero || this.IsClosed;

    protected override bool ReleaseHandle() => (uint) LibraryHandle.FreeLibrary(this.handle) > 0U;

    [SuppressUnmanagedCodeSecurity]
    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    private static extern int FreeLibrary([In] IntPtr hModule);

    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true, BestFitMapping = false)]
    private static extern IntPtr GetProcAddress([In] LibraryHandle hModule, [MarshalAs(UnmanagedType.LPStr), In] string lpProcName);

    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    private static extern uint GetLastError();

    protected void ThrowOnError() => throw new Win32Exception((int) LibraryHandle.GetLastError());

    protected IntPtr CheckEmptyHandle(IntPtr handle)
    {
      if (handle == IntPtr.Zero)
        this.ThrowOnError();
      return handle;
    }

    protected Delegate GetDelegate(string functionName, Type delegateType)
    {
      IntPtr procAddress = LibraryHandle.GetProcAddress(this, functionName);
      return !(procAddress == IntPtr.Zero) ? Marshal.GetDelegateForFunctionPointer(procAddress, delegateType) : throw new Win32Exception((int) LibraryHandle.GetLastError());
    }
  }
}
