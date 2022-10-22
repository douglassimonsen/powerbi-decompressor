// Decompiled with JetBrains decompiler
// Type: Microsoft.AnalysisServices.AdomdClient.XmlaStream
// Assembly: Microsoft.PowerBI.AdomdClient, Version=15.0.0.0, Culture=neutral, PublicKeyToken=89845dcd8080cc91
// MVID: F43CE853-F0F3-464F-BA39-D630D391E412
// Assembly location: C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.AdomdClient.dll

using System;
using System.IO;

namespace Microsoft.AnalysisServices.AdomdClient
{
  internal abstract class XmlaStream : Stream
  {
    protected bool disposed;
    private string sessionID = string.Empty;
    private bool isCompressionEnabled;
    private bool isSessionTokenNeeded;

    public new virtual void Dispose() => base.Dispose();

    public abstract void WriteEndOfMessage();

    public abstract void Skip();

    public abstract XmlaDataType GetResponseDataType();

    public abstract XmlaDataType GetRequestDataType();

    public virtual void WriteSoapActionHeader(string action)
    {
    }

    public virtual string GetExtendedErrorInfo() => string.Empty;

    public override bool CanRead => true;

    public override bool CanWrite => true;

    public override bool CanSeek => false;

    public override long Length => throw new NotSupportedException();

    public override long Position
    {
      get => throw new NotSupportedException();
      set => throw new NotSupportedException();
    }

    public virtual Guid ActivityID { get; set; }

    public virtual Guid RequestID { get; set; }

    public virtual Guid CurrentActivityID { get; set; }

    public override long Seek(long offset, SeekOrigin origin) => throw new NotSupportedException();

    public override void SetLength(long value) => throw new NotSupportedException();

    public virtual string SessionID
    {
      get => this.sessionID;
      set => this.sessionID = value;
    }

    public virtual bool IsSessionTokenNeeded
    {
      get => this.isSessionTokenNeeded;
      set => this.isSessionTokenNeeded = value;
    }

    public virtual bool IsCompressionEnabled
    {
      get => this.isCompressionEnabled;
      set => this.isCompressionEnabled = value;
    }

    public override IAsyncResult BeginWrite(
      byte[] buffer,
      int offset,
      int size,
      AsyncCallback callback,
      object state)
    {
      throw new NotSupportedException();
    }

    public override IAsyncResult BeginRead(
      byte[] buffer,
      int offset,
      int size,
      AsyncCallback callback,
      object state)
    {
      throw new NotSupportedException();
    }

    public override int EndRead(IAsyncResult asyncResult) => throw new NotSupportedException();

    public override void EndWrite(IAsyncResult asyncResult) => throw new NotSupportedException();

    private class Lock
    {
    }
  }
}
