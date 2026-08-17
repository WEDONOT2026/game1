[app]

title = 贪吃蛇
package.name = snakegame
package.domain = org.termux

source.dir = .
source.include_exts = py,png,jpg,json

version = 1.0.0

requirements = python3,pygame

orientation = portrait
fullscreen = 1

android.api = 33
android.minapi = 21
android.archs = arm64-v8a

android.permissions = INTERNET
android.accept_sdk_license = True

[buildozer]
log_level = 2
