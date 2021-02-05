using System;
using System.Collections;
using System.Collections.Generic;
using LegoSorter.MotorController.MultipleUploader.Models;

namespace MultipleUploaderTests
{
    public class ControllerData : IEnumerable<object[]>
    {
        public static IEnumerable<object[]> GetScaleControllerLCD()
        {
            yield return new object[] {new ControllerInfo("ScaleController2", "2", "192.168.178.87")};
            yield return new object[] {new ControllerInfo("ScaleController4", "4", "192.168.178.92")};
            yield return new object[] {new ControllerInfo("ScaleController6", "6", "192.168.178.95")};
            yield return new object[] {new ControllerInfo("ScaleController8", "8", "192.168.178.101")};
            yield return new object[] {new ControllerInfo("ScaleController10", "10", "192.168.178.111")};
            yield return new object[] {new ControllerInfo("ScaleController12", "12", "192.168.178.74")};
            yield return new object[] {new ControllerInfo("ScaleController14", "14", "192.168.178.105")};
            yield return new object[] {new ControllerInfo("ScaleController16", "16", "192.168.178.103")};
            yield return new object[] {new ControllerInfo("ScaleController18", "18", "192.168.178.107")};
            yield return new object[] {new ControllerInfo("ScaleController20", "20", "192.168.178.112")};
            yield return new object[] {new ControllerInfo("ScaleController22", "22", "192.168.178.90")};
            yield return new object[] {new ControllerInfo("ScaleController24", "24", "192.168.178.108")};
            yield return new object[] {new ControllerInfo("ScaleController26", "26", "192.168.178.109")};
            yield return new object[] {new ControllerInfo("ScaleController28", "28", "192.168.178.94")};
        } 
        
        public static IEnumerable<object[]> GetScaleControllerOLED()
        {
            yield return new object[] {new ControllerInfo("ScaleController1" ,"1","192.168.178.84")};
            yield return new object[] {new ControllerInfo("ScaleController3" ,"3","192.168.178.98")}; 
            yield return new object[] {new ControllerInfo("ScaleController5" ,"5","192.168.178.76")}; 
            yield return new object[] {new ControllerInfo("ScaleController7" ,"7","192.168.178.77")};
            yield return new object[] {new ControllerInfo("ScaleController9" ,"9","192.168.178.115")};
            yield return new object[] {new ControllerInfo("ScaleController11","11","192.168.178.117")};
            yield return new object[] {new ControllerInfo("ScaleController13","13","192.168.178.85")};
            yield return new object[] {new ControllerInfo("ScaleController15","15","192.168.178.88")};
            yield return new object[] {new ControllerInfo("ScaleController17","17","192.168.178.91")};
            yield return new object[] {new ControllerInfo("ScaleController19","19","192.168.178.79")};
            yield return new object[] {new ControllerInfo("ScaleController21","21","192.168.178.93")};
            yield return new object[] {new ControllerInfo("ScaleController23","23","192.168.178.89")};
            yield return new object[] {new ControllerInfo("ScaleController25","25","192.168.178.96")};
            yield return new object[] {new ControllerInfo("ScaleController27","27","192.168.178.97")};
        }
        
        public static IEnumerable<object[]> GetValveController()
        {
            
            yield return new object[] {new ControllerInfo("ValveController1", "1", "192.168.178.86") };
            yield return new object[] {new ControllerInfo("ValveController2", "2", "192.168.178.106") };
            yield return new object[] {new ControllerInfo("ValveController3", "3", "192.168.178.100") };
            yield return new object[] {new ControllerInfo("ValveController4", "4", "192.168.178.102") };
        }  
        
        public static IEnumerable<object[]> GetLifterController()
        {
            yield return new object[] {new ControllerInfo("LifterController", "1", "192.168.178.71") };
        }
        public static IEnumerable<object[]> GetVibrationController()
        {
            yield return new object[] {new ControllerInfo("VibrationController", "1", "192.168.178.70") };
           // yield return new object[] {new ControllerInfo("VibrationController", "1", "192.168.178.114") };
        } 
        public static IEnumerable<object[]> GetConveyorController()
        {
            yield return new object[] {new ControllerInfo("ConveyorController", "1", "192.168.178.72") };
        }


        public IEnumerator<object[]> GetEnumerator()
        {
            throw new NotImplementedException();
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return GetEnumerator();
        }
    }
}
