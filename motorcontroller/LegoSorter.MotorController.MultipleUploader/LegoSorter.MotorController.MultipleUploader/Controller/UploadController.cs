using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;
using LegoSorter.MotorController.MultipleUploader.Models;

namespace LegoSorter.MotorController.MultipleUploader.Controller
{
    public class UploadController : IUploadController
    {
        private readonly IBoardInfoController _boardInfoController;
        public UploadController(IBoardInfoController boardInfoController)
        {
            _boardInfoController = boardInfoController;
        }

        public List<string> FlashBoardOta(string folder, string deviceName, string deviceNumber, string deviceIp)
        {
            var newFirmwareVersion = GetNewFirmwareVersion(folder);
            if (newFirmwareVersion == GetFirmwareVersion(deviceIp))
            {
                return new List<string>() { "[SUCCESS]: Firmware " + newFirmwareVersion + " already on device " + deviceName };
            }
            ChangeBoardInfoFile(folder, deviceName, deviceNumber);
            ChangeUploaderInfoFile(folder, deviceIp, deviceName);

            return StartUpload(folder, deviceName);
        }

        private string GetNewFirmwareVersion(string folder)
        {
            string fileName = "boardinfo.h";
            string filepath = Path.Combine(folder, "src", fileName);

            var text = GetFileText(filepath, fileName);
            return ParseFirmwareVersion(text);
        }

        public string GetFirmwareVersion(string controllerInfoIp)
        {
            ControllerInfo info = _boardInfoController.GetStatus(controllerInfoIp);
            return info.Version;
        }

        private List<string> StartUpload(string folder, string deviceName)
        {
            var logfile = new List<string>();
            string fileName = "pio.exe";
            string filepath = Path.Combine(@"C:\Users\rhoffmann\.platformio\penv\Scripts\", fileName);
            if (Path.GetFileName(filepath) != fileName)
            {
                throw new Exception(fileName + "  not found!");
            }

            var proc = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = filepath,
                    Arguments = "run --target upload",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    CreateNoWindow = false,
                    WorkingDirectory = folder
                }
            };

            StringBuilder sb = new StringBuilder();

            proc.Start();
            while (!proc.StandardOutput.EndOfStream)
            {
                string line = proc.StandardOutput.ReadLine();
                sb.AppendLine(line);
                logfile.Add(line);
                
            }
            proc.WaitForExit();
            var logfolder = Path.Combine(folder, "uploadLogs", deviceName);
            CreateLogFolder(logfolder);
            File.WriteAllText(Path.Combine(logfolder, "uploadLog" + DateTime.Now.ToString("yyyy-MM-dd_Hmm") + ".txt"), sb.ToString());
            sb.Clear();
            return logfile;
        }

        private void CreateLogFolder(string logfolder)
        {
            System.IO.Directory.CreateDirectory(logfolder);
        }

        private void ChangeUploaderInfoFile(string folder, string deviceIp, string deviceName)
        {
            string fileName = "platformio.ini";
            string filepath = Path.Combine(folder,  fileName);

            var text = GetFileText(filepath, fileName);
            text = ModifyPlatformIni(text, deviceIp, deviceName);

            File.WriteAllText(filepath, text);
        }

        private void ChangeBoardInfoFile(string folder, string deviceName, string deviceNumber)
        {
            string fileName = "boardinfo.h";
            string filepath = Path.Combine(folder, "src", fileName);

            var text = GetFileText(filepath, fileName);
            text = ModifyBoardInfoText(text, deviceName, deviceNumber);

            File.WriteAllText(filepath, text);
        }

        private static string GetFileText(string filepath, string fileName)
        {
            if (Path.GetFileName(filepath) != fileName)
            {
                throw new Exception(fileName + "  not found!");
            }

            string text = File.ReadAllText(filepath);
            return text;
        }

        private string ModifyPlatformIni(string text, string deviceIp, string deviceName)
        {
            text = Regex.Replace(text, @"upload_port = .*", @"upload_port = " + deviceIp + " ;" + deviceName);
            return text;
        }

        private static string ModifyBoardInfoText(string text, string deviceName, string deviceNumber)
        {
            text =  Regex.Replace(text, @"BOARDNUMBER = ""\d+""", @"BOARDNUMBER = """ + deviceNumber + @"""");
            text =  Regex.Replace(text, @"CONTROLLERNAME = "".*""", @"CONTROLLERNAME = """ + deviceName +  @"""");
            return text;
        }

        private string ParseFirmwareVersion(string text)
        {
            var regex = new Regex(@"VERSION = ""(.*)""");
            return regex.Match(text).Groups[1].Value;
        }
    } 

    public interface IUploadController
    {
        List<string> FlashBoardOta(string folder, string deviceName, string deviceNumber, string deviceIp);
        string GetFirmwareVersion(string controllerInfoIp);
    }
}