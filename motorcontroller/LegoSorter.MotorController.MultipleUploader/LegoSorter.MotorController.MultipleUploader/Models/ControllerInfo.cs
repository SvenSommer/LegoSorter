namespace LegoSorter.MotorController.MultipleUploader.Models
{
    public class ControllerInfo
    {
        public ControllerInfo()
        {
        }

        public ControllerInfo(string name, string number, string ip)
        {
            Name = name;
            Number = number;
            Ip = ip;
        }
        public string Name { get; set; }
        public string Number { get; set; }
        public string Ip { get; set; }
        public string Version { get; set; }
    }
}