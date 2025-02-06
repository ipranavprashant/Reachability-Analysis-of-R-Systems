#  #Test Case 2.
#     agent_template = AgentTemplate(
#         L={"l0", "l1", "l2"},
#         initial_state="l0",
#         Act={"a1", "a2"},
#         P={"l0": {"a1"}, "l1": {"a2"}},
#         tr=[
#             ("l0", "a1", {"a1"}, "b", "l1"),
#             ("l1", "a2", {"a2"}, "b", "l2")
#         ],
#         leave="l2"
#     )

#     environment = Environment(
#         LE={"l_e"},
#         initial_state_E="l_e",
#         ActE={"b"},
#         PE={"l_e": {"b"}},
#         trE=[
#             ("l_e", "b", {"a1"}, "l_e"),
#             ("l_e", "b", {"a2"}, "l_e")
#         ]
#     )


#      #Test Case 3.
#     agent_template = AgentTemplate(
#         L={"l0", "l1", "l2"},
#         initial_state="l0",
#         Act={"a1", "a2"},
#         P={"l0": {"a1"}, "l1": {"a2"}},
#         tr=[
#             ("l0", "a1", set(), "b", "l1"),
#             ("l1", "a2", set(), "b", "l2")
#         ],
#         leave="l2"
#     )

#     environment = Environment(
#         LE={"l_e"},
#         initial_state_E="l_e",
#         ActE={"b"},
#         PE={"l_e": {"b"}},
#         trE=[
#             ("l_e", "b", {"a1"}, "l_e"),
#             ("l_e", "b", {"a2"}, "l_e")
#         ]
#     )