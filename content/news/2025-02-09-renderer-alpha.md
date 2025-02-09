---
layout: post
title: "A WIP renderer for robotics based on SDL3-GPU"
tags: rendering", "visualization", "robotics", "3D graphics
---

<video controls autoplay class="my-video">
    <source src="/ur5.mp4" type="video/mp4">
</video>

Recently, I made public a [new repo](https://github.com/ManifoldFR/candlewick) on GitHub, which is supposed to be a new renderer for robotics applications. It's very much a work in progress, read on for more details on the rationale behind it.


<!-- more -->

## Rationale

For a while, my colleagues and I have been discussing if we could find a satisfactory solution for rendering robot scenes in a window.
* It needed to be modern and cross-platform, supporting Metal on macOS and Vulkan on Linux (_maybe_ Windows in the future), with consistent behaviour.
* It also needed to be real-time capable.
* It needed be extendable with some interaction capabilities (adding sliders, buttons, such as the kind one can add with [ImGui](https://github.com/ocornut/imgui) or [egui](https://github.com/emilk/egui) in Rust-world).
* It needs to provide both C++ and Python APIs.
* It needs to have facilities to dump images or video.

Possible uses for such a renderer would be, visualizing trajectories for debugging motion generation algorithms, controllers, monitoring the behaviour of real-time controllers (MPC or RL), debugging and visualizing scenarios for a real-time physics simulator (like the upcoming [Simple](https://github.com/Simple-Robotics/simple)).

A good reason to support Vulkan, is support for complex modern real-time rendering workflows, more consistency in the way they behave across GPU vendors and OSes, and better performance. The OpenGL standard hasn't been updated by Khronos since 4.6 in 2016, and Apple itself stopped OpenGL support for macOS at 4.1 back in 2010 (Apple doing Apple things).

## Prior software

There's a host of software which already exists for robotics visualization.

Historically, there was [gepetto-viewer](https://github.com/Gepetto/gepetto-viewer), a viewer created for the Pinocchio and HPP suite of libraries based on the old [OpenSceneGraph](https://openscenegraph.github.io/openscenegraph.io/) (OSG) 3D toolkit, itself based on the classic OpenGL API and written in C++.
It has been used for offline trajectory visualization and replay, debugging planning algorithms, and so on.
While OSG has been deprecated for a few years and succeeded by [VulkanSceneGraph](https://vsg-dev.github.io/vsg-dev.io/) (VSG, name self-explanatory), gepetto-viewer is not really updated anymore apart from maintenance, and a transition to VSG was never made.  

Our team has been using [meshcat](https://github.com/meshcat-dev/meshcat) for the last few years as a stopgap replacement. It is a WebGL-based renderer running in the browser, using the ThreeJS toolkit which is essentially a middleware for WebGL (1.x and 2.x, with [still-evolving](https://www.youtube.com/watch?v=7we9mqIOKyw) WebGPU support).
Meshcat, and especially its [Python bindings](https://github.com/meshcat-dev/meshcat-python) don't seem to be maintained anymore.
The last release was never pushed to [PyPi](https://pypi.org/project/meshcat/), and no PRs have been accepted in months on either repo.
There is a C++ API as part of the [Drake framework](https://drake.mit.edu/doxygen_cxx/classdrake_1_1geometry_1_1_meshcat_visualizer.html) from TRI, although there was [an attempt](https://github.com/ami-iit/meshcat-cpp) to port it to a standalone package by some of our Italian colleagues.  
Our experience with meshcat-python had been okay, but with some major drawbacks that make it unsuitable for the full breadth of applications we want. It is _definitely_ not real-time capable, there is quite a bit of latency between e.g. changing the camera's pose matrix or changing a node in the scene, and getting the result on screen.
It has a rather complex structure: a Python client communicating with a server over ZeroMQ, which talks to the ThreeJS browser code by websocket...
Extending the visualizer (even statically) is quite painful due to this complex structure (which _might_ account for a bit of the Python API's latency): there's a mix of adding Python ZeroMQ commands which get transferred to JS as websocket messages.
Dynamic extensions are a no-go. There is basically no interaction capability beyond changing some flags in the scene tree. This might be fundamentally because it was never intended for such things.

We've also looked at [Rerun](https://rerun.io), a Rust-based multi-use data visualization framework which is properly cross-platform. This is thank to its use of the excellent [wgpu](https://wgpu.rs/), Mozilla's WebGPU implementation (it is also used by other projects such as the [bevy](https://bevyengine.org/) game engine).
I've even written a small [proof-of-concept library](https://github.com/ManifoldFR/pinocchio-rerun) for loading and visualizing Pinocchio models and geometries through Rerun.
At that point, customisability (adding rendering options, environments, skyboxes, interactibility...) came up as an issue.

## Custom software

[Simple Directmedia Layer (SDL)](https://libsdl.org/) is a wonderful, widely-used C library for writing multi-media applications such as games. It provides a host of systems for creating windows, programming keyboard, mouse, and gamepad interactions. It can be used to provide window contexts and surfaces for DirectX, OpenGL and Vulkan to render to.

Recently, the people behind SDL released [version 3](https://github.com/libsdl-org/SDL/releases/tag/release-3.2.0), which adds many improvements and features to the library.
One major addition is a new GPU API which dynamically wraps around modern graphics APIs Vulkan, DirectX 12, and Metal (much like the WebGPU implementations wgpu and [Dawn](https://github.com/google/dawn) do).

I decided to take a crack at building my own renderer using it. One advantage here is that we only have a single major dependency (SDL).

Turns out, it's really really hard (no sh!t). There's a whole lot of questions around code organization, loading assets (meshes, textures, shaders) and interacting with them, implementing cameras, and properly articulating this with the actual rendering.

I have virtually no experience with this stuff. I've messed around with writing one-shot OpenGL code and basic shaders in the past, with no thought towards factorization and making something that can actually be used.
Writing an actual renderer with tools, and loaders, and shaders is another story entirely.

Other dependencies which are useful to get things going include ImGui (mentiond above) for writing immediate-mode GUIs for interaction, assimp for loading assets (which our collision geometry and algorithms library [Coal](https://github.com/coal-library/coal) uses), and [EnTT](https://github.com/skypjack/entt) for organizing the way we render objects using an entity-component-systems (ECS) design.


-----

<div class="iframely-embed"><div class="iframely-responsive" style="padding-bottom: 50%; padding-top: 120px;"><a href="https://github.com/ManifoldFR/candlewick" data-iframely-url="//iframely.net/vWKCoW7"></a></div></div><script async src="//iframely.net/embed.js"></script>
