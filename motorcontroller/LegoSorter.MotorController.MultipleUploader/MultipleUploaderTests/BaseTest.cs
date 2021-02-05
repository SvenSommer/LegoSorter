using Xunit.Abstractions;

namespace MultipleUploaderTests
{
    public class BaseTest
    {
        private readonly ITestOutputHelper _output;
        public BaseTest(ITestOutputHelper output)
        {
            _output = output;
        }
    }
}