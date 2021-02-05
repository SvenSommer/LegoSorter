using LegoSorter.MotorController.MultipleUploader.Models;
using Newtonsoft.Json;
using RestSharp;

namespace LegoSorter.MotorController.MultipleUploader.Controller
{
    public class BoardInfoController : IBoardInfoController
    {
        public ControllerInfo GetStatus(string controllerInfoIp)
        {
            var client = new RestClient("http://" + controllerInfoIp + "/getstatus");
            client.Timeout = -1;
            var request = new RestRequest(Method.GET);
            IRestResponse response = client.Execute(request);
            var statusResponse = JsonConvert.DeserializeObject<StatusResponse>(response.Content);
            return MapSubstitutionResults(statusResponse);
        }

        private ControllerInfo MapSubstitutionResults(StatusResponse statusResponse)
        {
            if (statusResponse != null)
            {
                return new ControllerInfo()
                {
                    Name = statusResponse.client,
                    Ip = statusResponse.ip,
                    Version = statusResponse.version
                };
            }
            else
            {
                return new ControllerInfo();
            }
        }
    }

    public class StatusResponse
    {
        public string client { get; set; }
        public string ip { get; set; }
        public string version { get; set; }
    }

    public interface IBoardInfoController
    {
        ControllerInfo GetStatus(string controllerInfoIp);
    }
}
