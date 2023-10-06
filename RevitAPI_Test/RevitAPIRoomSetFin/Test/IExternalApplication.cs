using Autodesk.Revit.UI;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Reflection;
using System.Windows.Media.Imaging;

namespace Test
{
    class ExternalApplication : IExternalApplication
    {
        public Result OnShutdown(UIControlledApplication application)
        {
            return Result.Succeeded;
        }

        public Result OnStartup(UIControlledApplication application)
        {
            //Create Ribbon Tab
            application.CreateRibbonTab("Test_D");

            string path = Assembly.GetExecutingAssembly().Location;
            PushButtonData button = new PushButtonData("Button1", "SetRoomFinishes", path, "Test.Panel");

            RibbonPanel panel = application.CreateRibbonPanel("Test Daniel", "Daniel's Panel");

            //Add button image
            Uri imagePath = new Uri(@"C:\Users\danieldleal0\Documents\Revit_API\RevitAPI_Test\Test\icons8-teste-50.png");
            BitmapImage image = new BitmapImage(imagePath);

            PushButton pushButton = panel.AddItem(button) as PushButton;
            pushButton.LargeImage = image;

            return Result.Succeeded;
        }
    }
}
