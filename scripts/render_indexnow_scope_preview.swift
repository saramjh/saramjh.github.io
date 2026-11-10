import AppKit
import Foundation

// Original schematic of three distinct evidence categories from first-party PR #38/#39.
// The values are not a time series or a count of indexed pages/readers.
let locale = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "en"
guard ["en", "ko"].contains(locale) else { fatalError("Expected en or ko") }
let destination = CommandLine.arguments.count > 2 ? CommandLine.arguments[2] :
    "assets/img/dev-indexnow-image-scope-20261110/indexnow-scope-\(locale).png"
let w = 1200, h = 630
guard let bitmap = NSBitmapImageRep(
  bitmapDataPlanes: nil, pixelsWide: w, pixelsHigh: h,
  bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true,
  isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0
), let graphics = NSGraphicsContext(bitmapImageRep: bitmap) else { fatalError("Bitmap unavailable") }

NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = graphics
let bg = NSColor(srgbRed: 0.060, green: 0.096, blue: 0.138, alpha: 1)
let white = NSColor(srgbRed: 0.956, green: 0.975, blue: 0.977, alpha: 1)
let muted = NSColor(srgbRed: 0.696, green: 0.766, blue: 0.804, alpha: 1)
let line = NSColor(srgbRed: 0.215, green: 0.290, blue: 0.335, alpha: 1)
let orange = NSColor(srgbRed: 0.974, green: 0.705, blue: 0.416, alpha: 1)
let cyan = NSColor(srgbRed: 0.396, green: 0.847, blue: 0.816, alpha: 1)
let pale = NSColor(srgbRed: 0.773, green: 0.825, blue: 0.863, alpha: 1)
func rect(_ x: CGFloat, _ top: CGFloat, _ width: CGFloat, _ height: CGFloat, _ color: NSColor) {
  color.setFill()
  NSRect(x: x, y: CGFloat(h)-top-height, width: width, height: height).fill()
}
func draw(_ string: String, _ x: CGFloat, _ top: CGFloat, _ size: CGFloat, _ color: NSColor,
          _ weight: NSFont.Weight = .regular, _ maxWidth: CGFloat? = nil) {
  let font = NSFont.systemFont(ofSize: size, weight: weight)
  let style: [NSAttributedString.Key: Any] = [.font: font, .foregroundColor: color]
  let measured = (string as NSString).size(withAttributes: style).width
  if let maxWidth, measured > maxWidth { fatalError("Text overflow: \(string) \(measured) > \(maxWidth)") }
  (string as NSString).draw(at: NSPoint(x: x, y: CGFloat(h) - top - size*1.23), withAttributes: style)
}

rect(0, 0, 1200, 630, bg)
rect(0, 0, 12, 630, cyan)
draw("DEVELOPER FIELD NOTE   /   INDEXNOW", 64, 42, 22, cyan, .semibold, 1050)
let ko = locale == "ko"
let title = ko ? "이미지 한 장, URL 120개 전송" : "One PNG, 120 URL submissions"
let subtitle = ko ? "실제 제출과 수정 후 검사 결과를 따로 보자" : "Three outcomes with different evidence"
draw(title, 64, 94, ko ? 49 : 54, white, .bold, 1090)
draw(subtitle, 64, 176, 27, muted, .regular, 1070)
rect(64, 240, 1072, 2, line)

let groups: [(String, String, String, String, NSColor)] = ko
  ? [("실제 제출", "120", "URL · HTTP 200 접수", "#42760722178", orange),
     ("오프라인 재검사", "1", "URL · /portfolio/", "PR #39 테스트", cyan),
     ("수정 후 배포", "0", "변경된 URL · 전송 생략", "#42761734284", pale)]
  : [("ACTUAL SUBMISSION", "120", "URLs · HTTP 200 accepted", "#42760722178", orange),
     ("OFFLINE REPLAY", "1", "URL · /portfolio/", "PR #39 regression test", cyan),
     ("FINAL DEPLOYMENT", "0", "Changed URLs · no POST", "#42761734284", pale)]
let columns: [CGFloat] = [64, 433, 800]
for (index, item) in groups.enumerated() {
  let x = columns[index]
  draw(item.0, x, 278, ko ? 21 : 20, muted, .medium, 335)
  draw(item.1, x, 321, 102, item.4, .bold, 325)
  draw(item.2, x, 452, ko ? 19 : 19, white, .regular, 332)
  draw(item.3, x, 486, 19, muted, .regular, 332)
  if index < 2 { rect(x + 340, 279, 1.5, 246, line) }
}
rect(64, 545, 1072, 2, line)
draw(ko ? "출처: GitHub Actions와 PR #39 · 색인·방문자 수를 의미하지 않음"
        : "Sources: GitHub Actions and PR #39  ·  Not an indexing or traffic metric",
     64, 564, ko ? 18 : 18, muted, .regular, 1050)
graphics.flushGraphics()
NSGraphicsContext.restoreGraphicsState()
guard let encoded = bitmap.representation(using: .png, properties: [:]) else { fatalError("PNG failed") }
let url = URL(fileURLWithPath: destination)
try FileManager.default.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
try encoded.write(to: url, options: .atomic)
print("Rendered \(locale): \(w)x\(h), \(encoded.count) bytes -> \(destination)")
