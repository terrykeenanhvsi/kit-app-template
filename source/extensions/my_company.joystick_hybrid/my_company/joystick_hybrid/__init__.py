# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

from .extension import *

def __init__(self):
    self._lock = threading.Lock()
    self._callbacks = tuple()
    self._subscriptions = []
    self.bus = omni.kit.app.get_app().get_message_bus_event_stream()
    #self.MY_CUSTOM_EVENT = carb.events.type_from_string("my.custom.event")
    #self.sub1 = self.bus.create_subscription_to_push_by_type(self.MY_CUSTOM_EVENT, self.on_event)
    #self.sub2 = self.bus.create_subscription_to_pop_by_type(self.MY_CUSTOM_EVENT, self.on_event)
