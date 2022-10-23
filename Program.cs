using Microsoft.AnalysisServices.AdomdClient;

namespace HelloWorld{
  class Decompressor{
    public ushort decompressedBufferSize = 0;
    public ushort decompressedBufferOffset = 0;
    public byte[] compressedBuffer = new byte[(int) ushort.MaxValue];
    public byte[] decompressedBuffer = new byte[(int) ushort.MaxValue];
    public byte[] compressionHeader = new byte[8];
    IntPtr decompressHandle = new IntPtr();
    private XpressMethodsWrapper XpressWrapper = XpressMethodsWrapper.XpressWrapper;
    public Stream stream;
    public Decompressor(Stream streamIn){
      stream = streamIn;
    }
    public bool ReadCompressedPacket(){
      int offset1 = 0;
      int num1;
      for (; offset1 < 8; offset1 += num1){
        num1 = this.stream.Read(this.compressionHeader, offset1, 8 - offset1);
        if (num1 == 0){
          if (offset1 == 0){
            return false;
          }
          throw new Exception("Unknown");
        }
      }
      
      ushort decompressedDataSize = (ushort) ((uint) this.compressionHeader[0] + ((uint) this.compressionHeader[1] << 8));
      ushort compressedDataSize = (ushort) ((uint) this.compressionHeader[4] + ((uint) this.compressionHeader[5] << 8));
      bool flag = (ushort) 0 < compressedDataSize && (int) compressedDataSize < (int) decompressedDataSize;
      ushort num2 = flag ? compressedDataSize : decompressedDataSize;
      byte[] buffer = flag ? this.compressedBuffer : this.decompressedBuffer;
      int offset2 = 0;
      int num3;
      for (; offset2 < (int) num2; offset2 += num3){
        num3 = this.stream.Read(buffer, offset2, (int) num2 - offset2);
        if (num3 == 0){
          throw new Exception("Could not read all expected data");
        }
      }
      if (flag){
        this.Decompress((int) compressedDataSize, (int) decompressedDataSize);
      }
      this.decompressedBufferOffset = (ushort) 0;
      this.decompressedBufferSize = decompressedDataSize;
      return true;
    }
    private void Decompress(int compressedDataSize, int decompressedDataSize){
      int actualDecompressedSize = this.XpressWrapper.Decompress(
        this.decompressHandle, 
        this.compressedBuffer, 
        compressedDataSize, 
        this.decompressedBuffer, 
        decompressedDataSize, 
        decompressedDataSize
      );
      if (actualDecompressedSize != decompressedDataSize){
        Console.WriteLine($"{actualDecompressedSize} {decompressedDataSize} {compressedDataSize}");
        throw new Exception("Decompression Failed");
      }
    }
    public void Read(){
      while (this.decompressedBufferSize <= (ushort) 0){
        this.ReadCompressedPacket();
      }
    }
  }
  class Program {
    static void Main(string[] args){
      Stream streamToOpen = File.Open("api.pbix", FileMode.Open);
      new Decompressor(streamToOpen).Read();
    }
  }
}