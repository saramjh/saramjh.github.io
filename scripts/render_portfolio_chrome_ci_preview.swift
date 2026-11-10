import AppKit
import Foundation

// Source: first-party GitHub Actions runs #42747929262 and #42752895730.
// Two individually observed runs, not controlled performance benchmarks.
let output = CommandLine.arguments.count > 1
    ? CommandLine.arguments[1]
    : "assets/img/dev-playwright-ci-runner-chrome-20261110/setup-comparison-en.png"
let width = 1200
let height = 630
guard let bitmap = NSBitmapImageRep(
    bitmapDataPlanes: nil, pixelsWide: width, pixelsHigh: height,
    bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true,
    isPlanar: false, colorSpaceName: .deviceRGB,
    bytesPerRow: 0, bitsPerPixel: 0
), let context = NSGraphicsContext(bitmapImageRep: bitmap) else {
    fatalError("Could not create bitmap context")
}
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = context
let white = NSColor(srgbRed: 0.97, green: 0.98, blue: 0.99, alpha: 1)
let muted = NSColor(srgbRed: 0.70, green: 0.76, blue: 0.85, alpha: 1)
let navy = NSColor(srgbRed: 0.06, green: 0.11, blue: 0.18, alpha: 1)
let gold = NSColor(srgbRed: 0.91, green: 0.69, blue: 0.43, alpha: 1)
let teal = NSColor(srgbRed: 0.34, green: 0.83, blue: 0.77, alpha: 1)
let track = NSColor(srgbRed: 0.15, green: 0.22, blue: 0.30, alpha: 1)
func box(_ x: CGFloat, _ top: CGFloat, _ w: CGFloat, _ h: CGFloat,
         _ c: NSColor, _ radius: CGFloat = 0) {
    c.setFill()
    let rect = NSRect(x: x, y: CGFloat(height) - top - h, width: w, height: h)
    NSBezierPath(roundedRect: rect, xRadius: radius, yRadius: radius).fill()
}
func text(_ s: String, _ x: CGFloat, _ top: CGFloat, _ size: CGFloat,
          _ c: NSColor, _ weight: NSFont.Weight = .regular) {
    let f = NSFont.systemFont(ofSize: size, weight: weight)
    let attr: [NSAttributedString.Key: Any] = [.font: f, .foregroundColor: c]
    // AppKit drawing origin is bottom-left; arguments here are top-aligned.
    (s as NSString).draw(at: NSPoint(x: x, y: CGFloat(height) - top - size * 1.20),
                         withAttributes: attr)
}
box(0, 0, 1200, 630, navy)
box(0, 0, 16, 630, teal)
text("FIELD NOTE   /   GITHUB ACTIONS", 75, 49, 24, teal, .semibold)
text("Where CI time went", 75, 101, 60, white, .bold)
text("Playwright preparation vs. browser checks", 75, 184, 28, muted)
box(75, 244, 1050, 2, track)
text("Bundled Chromium download", 75, 268, 27, white, .medium)
box(75, 322, 834, 38, track, 7)
box(75, 322, 834, 38, gold, 7)
text("66 s", 948, 317, 38, white, .bold)
text("Runner-installed Chrome", 75, 383, 27, white, .medium)
box(75, 437, 834, 38, track, 7)
box(75, 437, 76, 38, teal, 7)
text("6 s", 948, 432, 38, white, .bold)
box(75, 512, 1050, 2, track)
text("Browser checks: 7 s before / 17 s after", 75, 531, 24, muted)
text("Runs 42747929262 / 42752895730  |  Single observed comparison", 75, 583, 20, muted)
context.flushGraphics()
NSGraphicsContext.restoreGraphicsState()
guard let data = bitmap.representation(using: .png, properties: [:]) else {
    fatalError("PNG encoding failed")
}
let destination = URL(fileURLWithPath: output)
try FileManager.default.createDirectory(at: destination.deletingLastPathComponent(),
    withIntermediateDirectories: true)
try data.write(to: destination, options: [.atomic])
print("Rendered \(output): \(width)x\(height), \(data.count) bytes")
