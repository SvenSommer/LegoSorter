using System.Collections.Generic;
using Autofac;
using LegoSorter.MotorController.MultipleUploader.Controller;

namespace LegoSorter.MotorController.MultipleUploader
{
    public class MultipleUploaderClient
    {
        private static IUploadController _app;

        public static MultipleUploaderClient Create()
        {
            var container = ContainerConfig.Configure();

            using (var scope = container.BeginLifetimeScope())
            {
                _app = scope.Resolve<IUploadController>();
            }
            return new MultipleUploaderClient();
        }

        public List<string> FlashBoardOta(string folder, string deviceName, string deviceNumber, string deviceIp)
        {
            return _app.FlashBoardOta(folder, deviceName, deviceNumber, deviceIp);
        }

        public string GetFirmwareVersion(string controllerInfoIp)
        {
            return _app.GetFirmwareVersion(controllerInfoIp);
        }
    }
}
