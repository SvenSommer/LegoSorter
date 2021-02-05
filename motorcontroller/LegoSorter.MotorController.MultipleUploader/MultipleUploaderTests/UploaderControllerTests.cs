using System.Collections.Generic;
using LegoSorter.MotorController.MultipleUploader;
using LegoSorter.MotorController.MultipleUploader.Models;
using Xunit;
using Xunit.Abstractions;

namespace MultipleUploaderTests
{
    public class UploaderControllerTests : BaseTest
    {
        private readonly ITestOutputHelper _output;

        public UploaderControllerTests(ITestOutputHelper output) : base(output)
        {
            _output = output;
        }


        [Theory]
        [MemberData(nameof(ControllerData.GetScaleControllerLCD), MemberType = typeof(ControllerData))]
        public void ShouldGetVersionsNumbersScalesLCD(ControllerInfo controllerInfo)
        {
            var client = MultipleUploaderClient.Create();
            string version = client.GetFirmwareVersion(controllerInfo.Ip);
            _output.WriteLine(controllerInfo.Name + ": Version:" + version);
            Assert.NotNull(version);
            Assert.NotEmpty(version);
        } 
        
        [Theory]
        [MemberData(nameof(ControllerData.GetScaleControllerOLED), MemberType = typeof(ControllerData))]
        public void ShouldGetVersionsNumbersScalesOLED(ControllerInfo controllerInfo)
        {
            var client = MultipleUploaderClient.Create();
            string version = client.GetFirmwareVersion(controllerInfo.Ip);
            _output.WriteLine(controllerInfo.Name + ": Version:" + version);
            Assert.NotNull(version);
            Assert.NotEmpty(version);
        }  

        [Theory]
        [MemberData(nameof(ControllerData.GetValveController), MemberType = typeof(ControllerData))]
        public void ShouldGetVersionsNumbersValveController(ControllerInfo controllerInfo)
        {
            var client = MultipleUploaderClient.Create();
            string version = client.GetFirmwareVersion(controllerInfo.Ip);
            _output.WriteLine(controllerInfo.Name + ": Version:" + version);
            Assert.NotNull(version);
            Assert.NotEmpty(version);
        }  
        
        [Theory]
        [MemberData(nameof(ControllerData.GetLifterController), MemberType = typeof(ControllerData))]
        [MemberData(nameof(ControllerData.GetVibrationController), MemberType = typeof(ControllerData))]
        [MemberData(nameof(ControllerData.GetConveyorController), MemberType = typeof(ControllerData))]
        public void ShouldGetVersionsProvidingSystems(ControllerInfo controllerInfo)
        {
            var client = MultipleUploaderClient.Create();
            string version = client.GetFirmwareVersion(controllerInfo.Ip);
            _output.WriteLine(controllerInfo.Name + ": Version:" + version);
            Assert.NotNull(version);
            Assert.NotEmpty(version);
        }

        [Theory]
        [MemberData(nameof(ControllerData.GetLifterController), MemberType = typeof(ControllerData))]
        public void ShouldUpdateFirmwareLifterController(ControllerInfo controllerInfo)
        {
            RunFirmwareUpload(controllerInfo, @"Y:\motorcontroller\PlatformIO\LifterControllerVNH7070AS");
        } 
        
        [Theory]
        [MemberData(nameof(ControllerData.GetVibrationController), MemberType = typeof(ControllerData))]
        public void ShouldUpdateFirmwareVibrationController(ControllerInfo controllerInfo)
        {
            RunFirmwareUpload(controllerInfo, @"Y:\motorcontroller\PlatformIO\V-FeederController");
        }  
        
        [Theory]
        [MemberData(nameof(ControllerData.GetConveyorController), MemberType = typeof(ControllerData))]
        public void ShouldUpdateFirmwareConveyorController(ControllerInfo controllerInfo)
        {
            RunFirmwareUpload(controllerInfo, @"Y:\motorcontroller\PlatformIO\ConveyorController");
        }    
        
        [Theory]
        [MemberData(nameof(ControllerData.GetScaleControllerLCD), MemberType = typeof(ControllerData))]
        public void ShouldUpdateFirmwareScaleControllerLCD(ControllerInfo controllerInfo)
        {
            RunFirmwareUpload(controllerInfo, @"Y:\motorcontroller\PlatformIO\ScaleControllerLCD");
        } 
        
        [Theory]
        [MemberData(nameof(ControllerData.GetScaleControllerOLED), MemberType = typeof(ControllerData))]
        public void ShouldUpdateFirmwareScaleControllerOLED(ControllerInfo controllerInfo)
        {
            RunFirmwareUpload(controllerInfo, @"Y:\motorcontroller\PlatformIO\ScaleControllerOLED");
        } 
        
        [Theory]
        [MemberData(nameof(ControllerData.GetValveController), MemberType = typeof(ControllerData))]
        public void ShouldUpdateFirmwareValveController(ControllerInfo controllerInfo)
        {
            RunFirmwareUpload(controllerInfo, @"Y:\motorcontroller\PlatformIO\ValveController");
        }

        private void RunFirmwareUpload(ControllerInfo controllerInfo, string pathToRessorce)
        {
            var client = MultipleUploaderClient.Create();
            var logfile = new List<string>()
            {
                "Start"
            };
            var retryCounter = 0;
            bool success = false;
            while (!logfile[^1].Contains("[SUCCESS]") && retryCounter < 4)
            {
                logfile = client.FlashBoardOta(pathToRessorce, controllerInfo.Name,
                    controllerInfo.Number, controllerInfo.Ip);
                retryCounter++;
                if (logfile[^1].Contains("[SUCCESS]"))
                {
                    success = true;
                    _output.WriteLine(retryCounter + ". run: SUCCESS");
                }
                else
                {
                    _output.WriteLine(retryCounter + ". run: FAILURE");
                }
            }

            _output.WriteLine("");
            _output.WriteLine("Details:");
            for (int i = logfile.Count - 1; i >= 0; i--)
            {
                _output.WriteLine(logfile[i]);
            }

            Assert.True(success);
        }
    }
}
