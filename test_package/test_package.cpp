// One sample through an IPC publish-subscribe service.
#include <cstdint>
#include <cstdio>
#include <string>

#include <unistd.h>

#include "iox2/node.hpp"
#include "iox2/sample_mut.hpp"
#include "iox2/service_name.hpp"

int main() {
  const std::string name = "conan/test_package/" + std::to_string(::getpid());
  auto node = iox2::NodeBuilder().create<iox2::ServiceType::Ipc>().value();
  auto service = node.service_builder(iox2::ServiceName::create(name.c_str()).value())
                     .publish_subscribe<std::uint64_t>()
                     .open_or_create()
                     .value();
  auto publisher = service.publisher_builder().create().value();
  auto subscriber = service.subscriber_builder().create().value();
  auto sample = publisher.loan().value();
  sample.payload_mut() = 4711U;
  if (!iox2::send(std::move(sample)).has_value()) return 1;
  auto received = subscriber.receive().value();
  if (!received.has_value() || received->payload() != 4711U) {
    std::printf("iceoryx2 test_package: FAIL\n");
    return 1;
  }
  std::printf("iceoryx2 test_package: PASS\n");
  return 0;
}
