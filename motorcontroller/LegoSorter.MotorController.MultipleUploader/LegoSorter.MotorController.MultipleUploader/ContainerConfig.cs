using Autofac;
using LegoSorter.MotorController.MultipleUploader.Controller;

namespace LegoSorter.MotorController.MultipleUploader
{
    public static class ContainerConfig
    {
        public static IContainer Configure()
        {
            var builder = new ContainerBuilder();

            builder.RegisterType<UploadController>().As<IUploadController>();
            builder.RegisterType<BoardInfoController>().As<IBoardInfoController>();
            
            return builder.Build();
        }

    }
}