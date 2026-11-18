import AppKit
import Foundation

let width = 1200
let height = 630

struct Copy {
    let title: String
    let summary: String
    let leftTitle: String
    let leftFirst: String
    let leftSecond: String
    let leftDetail: String
    let rightTitle: String
    let rightFirst: String
    let rightSecond: String
    let rightDetail: String
    let caveat: String
}

func color(_ hex: Int) -> NSColor {
    return NSColor(calibratedRed: CGFloat((hex >> 16) & 255) / 255,
                   green: CGFloat((hex >> 8) & 255) / 255,
                   blue: CGFloat(hex & 255) / 255,
                   alpha: 1.0)
}

func rect(_ x: CGFloat, _ top: CGFloat, _ w: CGFloat, _ h: CGFloat,
          fill: NSColor, radius: CGFloat = 0) {
    fill.setFill()
    let area = NSRect(x: x, y: CGFloat(height) - top - h, width: w, height: h)
    NSBezierPath(roundedRect: area, xRadius: radius, yRadius: radius).fill()
}

func draw(_ value: String, _ x: CGFloat, _ top: CGFloat, _ w: CGFloat,
          _ h: CGFloat, size: CGFloat, shade: NSColor, bold: Bool = false) {
    let font = NSFont.systemFont(ofSize: size, weight: bold ? .semibold : .regular)
    let p = NSMutableParagraphStyle()
    p.lineBreakMode = .byWordWrapping
    p.alignment = .left
    (value as NSString).draw(
        in: NSRect(x: x, y: CGFloat(height) - top - h, width: w, height: h),
        withAttributes: [.font: font, .foregroundColor: shade, .paragraphStyle: p]
    )
}

let isKorean = CommandLine.arguments.count > 1 && CommandLine.arguments[1] == "ko"
let root = CommandLine.arguments.count > 2 ? CommandLine.arguments[2] : "."
let text: Copy
if isKorean {
    text = Copy(
        title: "홈 화면 앱과 검색 상태 복원",
        summary: "Spoonie PR #47  ·  변경 동작 요약",
        leftTitle: "01  홈 화면 앱",
        leftFirst: "앱 실행 · 다시 온라인",
        leftSecond: "서비스 워커 업데이트 확인",
        leftDetail: "작성 중에는 자동 새로고침 방지",
        rightTitle: "02  레시피 검색",
        rightFirst: "검색 결과 → 레시피 상세 → 뒤로",
        rightSecond: "URL의 검색어와 탭 복원",
        rightDetail: "첫 페이지부터 결과 수 표시",
        caveat: "실제 제품 화면이 아닌 구현 흐름 도식 · iPhone 실기기 테스트는 미실시"
    )
} else {
    text = Copy(
        title: "PWA updates & search state",
        summary: "Spoonie PR #47  ·  A diagram of the implemented flows",
        leftTitle: "01  Home Screen app",
        leftFirst: "Open app · reconnect online",
        leftSecond: "Check for service-worker updates",
        leftDetail: "Avoid auto-reload while editing",
        rightTitle: "02  Recipe search",
        rightFirst: "Results → Recipe detail → Back",
        rightSecond: "Restore query and tab from URL",
        rightDetail: "Show counts from the first page",
        caveat: "Implementation diagram, not an app screenshot · Physical iPhone not tested"
    )
}

guard let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil,
                                   pixelsWide: width, pixelsHigh: height,
                                   bitsPerSample: 8, samplesPerPixel: 4,
                                   hasAlpha: true, isPlanar: false,
                                   colorSpaceName: .deviceRGB,
                                   bytesPerRow: 0, bitsPerPixel: 0),
      let graphics = NSGraphicsContext(bitmapImageRep: bitmap) else {
    fatalError("Unable to initialize graphics bitmap")
}
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = graphics
graphics.imageInterpolation = .high

let ink = color(0x193139)
let muted = color(0x50646A)
let teal = color(0x0A7377)
let border = color(0xC3D4D1)
let paper = color(0xF5F5F0)
let card = color(0xFFFFFF)

rect(0, 0, 1200, 630, fill: paper)
rect(0, 0, 1200, 9, fill: teal)
rect(55, 41, 8, 26, fill: teal, radius: 4)
draw("SPOONIE", 75, 37, 300, 36, size: 25, shade: ink, bold: true)
draw("DEVELOPER NOTE  /  2026.11.16", 780, 41, 360, 28, size: 17, shade: muted)

draw(text.title, 55, 100, 1095, 73, size: isKorean ? 52 : 51, shade: ink, bold: true)
draw(text.summary, 59, 175, 1050, 40, size: 25, shade: muted)
rect(55, 234, 530, 275, fill: card, radius: 18)
rect(615, 234, 530, 275, fill: card, radius: 18)
rect(74, 254, 10, 43, fill: teal, radius: 5)
rect(634, 254, 10, 43, fill: teal, radius: 5)

draw(text.leftTitle, 102, 254, 445, 49, size: 30, shade: ink, bold: true)
draw(text.rightTitle, 662, 254, 445, 49, size: 30, shade: ink, bold: true)
draw(text.leftFirst, 90, 330, 465, 34, size: isKorean ? 24 : 23, shade: muted)
draw(text.rightFirst, 650, 330, 470, 34, size: isKorean ? 23 : 22, shade: muted)
rect(90, 382, 465, 2, fill: border)
rect(650, 382, 465, 2, fill: border)
draw(text.leftSecond, 90, 404, 460, 42, size: isKorean ? 27 : 25, shade: teal, bold: true)
draw(text.rightSecond, 650, 404, 470, 42, size: isKorean ? 27 : 25, shade: teal, bold: true)
draw(text.leftDetail, 90, 464, 465, 31, size: 20, shade: muted)
draw(text.rightDetail, 650, 464, 470, 31, size: 20, shade: muted)

rect(55, 548, 1090, 2, fill: border)
draw(text.caveat, 57, 569, 1090, 35, size: isKorean ? 18 : 19, shade: muted)

NSGraphicsContext.restoreGraphicsState()
guard let data = bitmap.representation(using: .png, properties: [:]) else {
    fatalError("Unable to encode PNG")
}
let dest = URL(fileURLWithPath: root)
    .appendingPathComponent("assets/img/dev/spoonie-pr47-pwa-og-20261118")
    .appendingPathComponent(isKorean ? "spoonie-pr47-ko.png" : "spoonie-pr47-en.png")
try data.write(to: dest, options: .atomic)
print("\(dest.path) \(data.count) bytes")
