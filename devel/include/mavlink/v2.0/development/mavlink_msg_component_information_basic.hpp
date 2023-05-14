// MESSAGE COMPONENT_INFORMATION_BASIC support class

#pragma once

namespace mavlink {
namespace development {
namespace msg {

/**
 * @brief COMPONENT_INFORMATION_BASIC message
 *
 * Basic component information data. Should be requested using MAV_CMD_REQUEST_MESSAGE on startup, or when required.
 */
struct COMPONENT_INFORMATION_BASIC : mavlink::Message {
    static constexpr msgid_t MSG_ID = 396;
    static constexpr size_t LENGTH = 156;
    static constexpr size_t MIN_LENGTH = 156;
    static constexpr uint8_t CRC_EXTRA = 129;
    static constexpr auto NAME = "COMPONENT_INFORMATION_BASIC";


    uint32_t time_boot_ms; /*< [ms] Timestamp (time since system boot). */
    uint64_t capabilities; /*<  Component capability flags */
    std::array<char, 32> vendor_name; /*<  Name of the component vendor. Needs to be zero terminated. The field is optional and can be empty/all zeros. */
    std::array<char, 32> model_name; /*<  Name of the component model. Needs to be zero terminated. The field is optional and can be empty/all zeros. */
    std::array<char, 24> software_version; /*<  Software version. The recommended format is SEMVER: 'major.minor.patch'  (any format may be used). The field must be zero terminated if it has a value. The field is optional and can be empty/all zeros. */
    std::array<char, 24> hardware_version; /*<  Hardware version. The recommended format is SEMVER: 'major.minor.patch'  (any format may be used). The field must be zero terminated if it has a value. The field is optional and can be empty/all zeros. */
    std::array<char, 32> serial_number; /*<  Hardware serial number. The field must be zero terminated if it has a value. The field is optional and can be empty/all zeros. */


    inline std::string get_name(void) const override
    {
            return NAME;
    }

    inline Info get_message_info(void) const override
    {
            return { MSG_ID, LENGTH, MIN_LENGTH, CRC_EXTRA };
    }

    inline std::string to_yaml(void) const override
    {
        std::stringstream ss;

        ss << NAME << ":" << std::endl;
        ss << "  time_boot_ms: " << time_boot_ms << std::endl;
        ss << "  capabilities: " << capabilities << std::endl;
        ss << "  vendor_name: \"" << to_string(vendor_name) << "\"" << std::endl;
        ss << "  model_name: \"" << to_string(model_name) << "\"" << std::endl;
        ss << "  software_version: \"" << to_string(software_version) << "\"" << std::endl;
        ss << "  hardware_version: \"" << to_string(hardware_version) << "\"" << std::endl;
        ss << "  serial_number: \"" << to_string(serial_number) << "\"" << std::endl;

        return ss.str();
    }

    inline void serialize(mavlink::MsgMap &map) const override
    {
        map.reset(MSG_ID, LENGTH);

        map << capabilities;                  // offset: 0
        map << time_boot_ms;                  // offset: 8
        map << vendor_name;                   // offset: 12
        map << model_name;                    // offset: 44
        map << software_version;              // offset: 76
        map << hardware_version;              // offset: 100
        map << serial_number;                 // offset: 124
    }

    inline void deserialize(mavlink::MsgMap &map) override
    {
        map >> capabilities;                  // offset: 0
        map >> time_boot_ms;                  // offset: 8
        map >> vendor_name;                   // offset: 12
        map >> model_name;                    // offset: 44
        map >> software_version;              // offset: 76
        map >> hardware_version;              // offset: 100
        map >> serial_number;                 // offset: 124
    }
};

} // namespace msg
} // namespace development
} // namespace mavlink
