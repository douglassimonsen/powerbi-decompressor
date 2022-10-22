// Decompiled with JetBrains decompiler
// Type: Microsoft.AnalysisServices.AdomdClient.XmlaStreamException
// Assembly: Microsoft.PowerBI.AdomdClient, Version=15.0.0.0, Culture=neutral, PublicKeyToken=89845dcd8080cc91
// MVID: F43CE853-F0F3-464F-BA39-D630D391E412
// Assembly location: C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.AdomdClient.dll

using System;
using System.IO;

namespace Microsoft.AnalysisServices.AdomdClient
{
  internal sealed class XmlaStreamException : IOException
  {
    private ConnectionExceptionCause connectionExceptionCause;

    internal ConnectionExceptionCause ConnectionExceptionCause => this.connectionExceptionCause;

    internal XmlaStreamException(string message)
      : base(message)
    {
    }

    internal XmlaStreamException(string message, Exception innerException)
      : base(message, innerException)
    {
    }

    internal XmlaStreamException(Exception innerException)
      : base(string.Empty, innerException)
    {
    }

    internal XmlaStreamException(
      Exception innerException,
      ConnectionExceptionCause connectionExceptionCause)
      : this(innerException)
    {
      this.connectionExceptionCause = connectionExceptionCause;
    }
  }
}
