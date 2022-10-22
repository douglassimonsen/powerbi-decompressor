// Decompiled with JetBrains decompiler
// Type: Microsoft.AnalysisServices.AdomdClient.CompressedStream
// Assembly: Microsoft.PowerBI.AdomdClient, Version=15.0.0.0, Culture=neutral, PublicKeyToken=89845dcd8080cc91
// MVID: F43CE853-F0F3-464F-BA39-D630D391E412
// Assembly location: C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.PowerBI.AdomdClient.dll

using System;
using System.ComponentModel;
using System.IO;

namespace Microsoft.AnalysisServices.AdomdClient
{
  internal class CompressedStream
  {
    private Stream baseStream;
    private IntPtr compressHandle = IntPtr.Zero;
    private IntPtr decompressHandle = IntPtr.Zero;
    private bool disposed = false;
    private byte[] compressionHeader;
    private byte[] compressedBuffer;
    private byte[] decompressedBuffer;
    private ushort decompressedBufferOffset;
    private ushort decompressedBufferSize;
    private const ushort WriteBufferFlushThreshold = 65535;
    private ushort writeCacheOffset = 8;
    private int compressionLevel;
    private XpressMethodsWrapper xpressWrapper;

    private XpressMethodsWrapper XpressWrapper
    {
      get
      {
        if (this.xpressWrapper == null)
          this.xpressWrapper = XpressMethodsWrapper.XpressWrapper;
        return this.xpressWrapper;
      }
    }

    internal CompressedStream(Stream stream, int compressionLevel)
    {
      try
      {
        this.baseStream = stream;
        this.compressionLevel = compressionLevel;
      }
      catch (Win32Exception ex)
      {
        throw new XmlaStreamException((Exception) ex);
      }
    }

    internal Stream BaseStream => this.baseStream;

    public bool IsCompressionEnabled
    {
      get => this.baseStream.IsCompressionEnabled;
      set => this.baseStream.IsCompressionEnabled = value;
    }

    public string SessionID
    {
      get => this.baseStream.SessionID;
      set => this.baseStream.SessionID = value;
    }

    public bool IsSessionTokenNeeded
    {
      get => this.baseStream.IsSessionTokenNeeded;
      set => this.baseStream.IsSessionTokenNeeded = value;
    }

    public Guid ActivityID
    {
      get => this.baseStream.ActivityID;
      set => this.baseStream.ActivityID = value;
    }

    public Guid RequestID
    {
      get => this.baseStream.RequestID;
      set => this.baseStream.RequestID = value;
    }

    public bool CanTimeout => this.baseStream.CanTimeout;

    public int ReadTimeout
    {
      get => this.baseStream.ReadTimeout;
      set => this.baseStream.ReadTimeout = value;
    }

    public virtual void SetBaseStream(Stream stream)
    {
      try
      {
        if (this.baseStream == stream)
          return;
        if (this.baseStream != null)
          this.baseStream.Dispose();
        this.baseStream = stream;
      }
      catch (Win32Exception ex)
      {
        throw new XmlaStreamException((Exception) ex);
      }
    }

    public XmlaDataType GetResponseDataType()
    {
      try
      {
        switch (this.baseStream.GetResponseDataType())
        {
          case XmlaDataType.BinaryXml:
          case XmlaDataType.CompressedBinaryXml:
            return XmlaDataType.BinaryXml;
          default:
            return XmlaDataType.TextXml;
        }
      }
      catch (Win32Exception ex)
      {
        throw new XmlaStreamException((Exception) ex);
      }
    }

    public XmlaDataType GetRequestDataType()
    {
      try
      {
        switch (this.baseStream.GetRequestDataType())
        {
          case XmlaDataType.BinaryXml:
          case XmlaDataType.CompressedBinaryXml:
            return XmlaDataType.BinaryXml;
          default:
            return XmlaDataType.TextXml;
        }
      }
      catch (Win32Exception ex)
      {
        throw new XmlaStreamException((Exception) ex);
      }
    }

    public void WriteSoapActionHeader(string action)
    {
      if (this.baseStream == null)
        return;
      this.baseStream.WriteSoapActionHeader(action);
    }

    public string GetExtendedErrorInfo() => this.baseStream == null ? string.Empty : this.baseStream.GetExtendedErrorInfo();

    public void Close() => this.baseStream.Close();

    public void Dispose() => this.Dispose(true);

    protected void Dispose(bool disposing)
    {
      if (this.disposed)
        return;
      try
      {
        this.CloseCompressionHandlesAndBuffers();
        if (disposing)
          this.baseStream.Dispose();
        this.xpressWrapper = (XpressMethodsWrapper) null;
        this.disposed = true;
        if (!disposing)
          return;
        GC.SuppressFinalize((object) this);
      }
      catch (IOException ex)
      {
      }
      catch (Win32Exception ex)
      {
      }
      finally
      {
        base.Dispose(disposing);
      }
    }

    ~CompressedStream() => this.Dispose(false);

    public void WriteEndOfMessage()
    {
      if (this.disposed)
        throw new ObjectDisposedException((string) null);
      try
      {
        if (this.CompressedWriteEnabled && this.writeCacheOffset > (ushort) 8)
          this.FlushCache();
        this.baseStream.WriteEndOfMessage();
      }
      catch (Win32Exception ex)
      {
        throw new XmlaStreamException((Exception) ex);
      }
    }

    public void Write(byte[] buffer, int offset, int size)
    {
      if (this.disposed)
        throw new ObjectDisposedException((string) null);
      if (buffer == null)
        throw new ArgumentNullException(nameof (buffer));
      if (offset < 0)
        throw new ArgumentOutOfRangeException(nameof (offset));
      if (size < 0)
        throw new ArgumentOutOfRangeException(nameof (size));
      if (size + offset > buffer.Length)
        throw new ArgumentException(XmlaSR.InvalidArgument, nameof (buffer));
      if (!this.CompressedWriteEnabled)
      {
        this.baseStream.Write(buffer, offset, size);
      }
      else
      {
        try
        {
          if (this.compressHandle == IntPtr.Zero)
            this.InitCompress();
          int val2 = size;
          int srcOffset = offset;
          ushort count;
          for (; val2 > 0; val2 -= (int) count)
          {
            if (this.writeCacheOffset >= ushort.MaxValue)
              this.FlushCache();
            count = (ushort) Math.Min((int) ushort.MaxValue - (int) this.writeCacheOffset, val2);
            Buffer.BlockCopy((Array) buffer, srcOffset, (Array) this.decompressedBuffer, (int) this.writeCacheOffset, (int) count);
            this.writeCacheOffset += count;
            srcOffset += (int) count;
          }
        }
        catch (Win32Exception ex)
        {
          throw new XmlaStreamException((Exception) ex);
        }
      }
    }

    public int Read(byte[] buffer, int offset, int size)
    {
      if (this.disposed)
        throw new ObjectDisposedException((string) null);
      if (buffer == null)
        throw new ArgumentNullException(nameof (buffer));
      if (offset < 0)
        throw new ArgumentOutOfRangeException(nameof (offset));
      if (size < 0)
        throw new ArgumentOutOfRangeException(nameof (size));
      if (size + offset > buffer.Length)
        throw new ArgumentException(XmlaSR.InvalidArgument, nameof (buffer));
      if (size == 0)
        return 0;
      try
      {
        int num = 0;
        if (this.decompressedBufferSize > (ushort) 0)
        {
          num = this.ReadFromCache(buffer, offset, size);
        }
        else
        {
          XmlaDataType responseDataType = Microsoft.AnalysisServices.AdomdClient.XmlaDataType.CompressedBinaryXml;
          switch (responseDataType)
          {
            case XmlaDataType.Undetermined:
              break;
            case XmlaDataType.TextXml:
            case XmlaDataType.BinaryXml:
              num = this.baseStream.Read(buffer, offset, size);
              break;
            case XmlaDataType.CompressedXml:
            case XmlaDataType.CompressedBinaryXml:
              if (this.decompressHandle == IntPtr.Zero)
                this.InitDecompress();
              do
                ;
              while (this.decompressedBufferSize <= (ushort) 0 && this.ReadCompressedPacket());
              if (this.decompressedBufferSize > (ushort) 0)
              {
                num = this.ReadFromCache(buffer, offset, size);
                break;
              }
              break;
            default:
              // ISSUE: reference to a compiler-generated method
              throw new NotImplementedException(XmlaSR.UnsupportedDataFormat(responseDataType.ToString()));
          }
        }
        return num;
      }
      catch (Win32Exception ex)
      {
        throw new XmlaStreamException((Exception) ex);
      }
    }

    public void Skip()
    {
      if (this.disposed)
        throw new ObjectDisposedException((string) null);
      this.baseStream.Skip();
      this.decompressedBufferOffset = (ushort) 0;
      this.decompressedBufferSize = (ushort) 0;
    }

    public void Flush()
    {
      if (this.disposed)
        throw new ObjectDisposedException((string) null);
      try
      {
        if (this.CompressedWriteEnabled && this.writeCacheOffset > (ushort) 8)
          this.FlushCache();
        this.baseStream.Flush();
      }
      catch (Win32Exception ex)
      {
        throw new XmlaStreamException((Exception) ex);
      }
    }

    private void InitDecompress()
    {
      if (this.decompressHandle != IntPtr.Zero)
        this.XpressWrapper.DecompressClose(this.decompressHandle);
      this.decompressHandle = this.XpressWrapper.DecompressInit();
      if (this.decompressHandle == IntPtr.Zero)
        throw new XmlaStreamException(XmlaSR.Decompression_InitializationFailed);
      if (this.decompressedBuffer != null)
        return;
      this.InitCompressionBuffers();
    }

    private void InitCompressionBuffers()
    {
      this.compressedBuffer = new byte[(int) ushort.MaxValue];
      this.decompressedBuffer = new byte[(int) ushort.MaxValue];
      this.compressionHeader = new byte[8];
    }

    private void Decompress(int compressedDataSize, int decompressedDataSize)
    {
      int actualDecompressedSize = this.XpressWrapper.Decompress(this.decompressHandle, this.compressedBuffer, compressedDataSize, this.decompressedBuffer, decompressedDataSize, decompressedDataSize);
      if (actualDecompressedSize != decompressedDataSize)
      {
        // ISSUE: reference to a compiler-generated method
        throw new XmlaStreamException(XmlaSR.Decompression_Failed(compressedDataSize, decompressedDataSize, actualDecompressedSize));
      }
    }

    private void CloseCompressionHandlesAndBuffers()
    {
      if (this.compressHandle != IntPtr.Zero)
      {
        this.XpressWrapper.CompressClose(this.compressHandle);
        this.compressHandle = IntPtr.Zero;
      }
      if (this.decompressHandle != IntPtr.Zero)
      {
        this.XpressWrapper.DecompressClose(this.decompressHandle);
        this.decompressHandle = IntPtr.Zero;
      }
      this.compressionHeader = (byte[]) null;
      this.compressedBuffer = (byte[]) null;
      this.decompressedBuffer = (byte[]) null;
      this.decompressedBufferOffset = (ushort) 0;
      this.decompressedBufferSize = (ushort) 0;
    }

    private bool ReadCompressedPacket()
    {
      int offset1 = 0;
      int num1;
      for (; offset1 < 8; offset1 += num1)
      {
        num1 = this.baseStream.Read(this.compressionHeader, offset1, 8 - offset1);
        if (num1 == 0)
        {
          if (offset1 == 0)
            return false;
          throw new Exception(XmlaSR.UnknownServerResponseFormat);
        }
      }
      ushort decompressedDataSize = (ushort) ((uint) this.compressionHeader[0] + ((uint) this.compressionHeader[1] << 8));
      ushort compressedDataSize = (ushort) ((uint) this.compressionHeader[4] + ((uint) this.compressionHeader[5] << 8));
      bool flag = (ushort) 0 < compressedDataSize && (int) compressedDataSize < (int) decompressedDataSize;
      ushort num2 = flag ? compressedDataSize : decompressedDataSize;
      byte[] buffer = flag ? this.compressedBuffer : this.decompressedBuffer;
      int offset2 = 0;
      int num3;
      for (; offset2 < (int) num2; offset2 += num3)
      {
        num3 = this.baseStream.Read(buffer, offset2, (int) num2 - offset2);
        if (num3 == 0)
          throw new Exception(XmlaSR.UnknownServerResponseFormat);
      }
      if (flag)
        this.Decompress((int) compressedDataSize, (int) decompressedDataSize);
      this.decompressedBufferOffset = (ushort) 0;
      this.decompressedBufferSize = decompressedDataSize;
      return true;
    }

    private int ReadFromCache(byte[] buffer, int offset, int size)
    {
      int count = Math.Min((int) this.decompressedBufferSize, size);
      Buffer.BlockCopy((Array) this.decompressedBuffer, (int) this.decompressedBufferOffset, (Array) buffer, offset, count);
      this.decompressedBufferSize -= (ushort) count;
      this.decompressedBufferOffset += (ushort) count;
      return count;
    }

    private bool CompressedWriteEnabled
    {
      get
      {
        if (this.baseStream == null)
          return false;
        XmlaDataType requestDataType = Microsoft.AnalysisServices.AdomdClient.XmlaDataType.CompressedBinaryXml;
        return requestDataType == XmlaDataType.CompressedXml || requestDataType == XmlaDataType.CompressedBinaryXml;
      }
    }

    private void InitCompress()
    {
      if (!(this.compressHandle == IntPtr.Zero))
        return;
      this.compressHandle = this.XpressWrapper.CompressInit(65536, this.compressionLevel);
      if (this.compressHandle == IntPtr.Zero)
        throw new XmlaStreamException(XmlaSR.Compression_InitializationFailed);
      this.InitCompressionBuffers();
    }

    private void FlushCache()
    {
      int num1 = (int) this.writeCacheOffset - 8;
      int num2 = this.XpressWrapper.Compress(this.compressHandle, this.decompressedBuffer, 8, num1, this.compressedBuffer, 8, num1);
      byte[] buffer;
      int count;
      if (0 < num2 && num2 < num1)
      {
        buffer = this.compressedBuffer;
        count = num2 + 8;
      }
      else
      {
        buffer = this.decompressedBuffer;
        count = (int) this.writeCacheOffset;
      }
      buffer[0] = (byte) (num1 & (int) byte.MaxValue);
      buffer[1] = (byte) (num1 >> 8 & (int) byte.MaxValue);
      buffer[2] = (byte) 0;
      buffer[3] = (byte) 0;
      buffer[4] = (byte) (num2 & (int) byte.MaxValue);
      buffer[5] = (byte) (num2 >> 8 & (int) byte.MaxValue);
      buffer[6] = (byte) 0;
      buffer[7] = (byte) 0;
      this.baseStream.Write(buffer, 0, count);
      this.writeCacheOffset = (ushort) 8;
    }
  }
}
