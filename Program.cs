using Microsoft.AnalysisServices.AdomdClient;

namespace HelloWorld {
  class Program {
   static void Open(){
      Stream streamToOpen = (Stream) File.Open("api.pbix", FileMode.Open);
      new CompressedStream((XmlaStream) streamToOpen, 0);
    }
    static void Main(string[] args){
       Open();
    }
  }
}