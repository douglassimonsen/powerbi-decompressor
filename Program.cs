using Microsoft.AnalysisServices.AdomdClient;

namespace HelloWorld{
  class Program {
   static void Open(){
      Stream streamToOpen = File.Open("api.pbix", FileMode.Open);
      CompressedStream stream3 = new CompressedStream(streamToOpen, 0);
    }
    static void Main(string[] args){
       Open();
    }
  }
}