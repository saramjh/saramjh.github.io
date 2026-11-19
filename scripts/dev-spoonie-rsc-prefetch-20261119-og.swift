import AppKit
import Foundation

let width = 1200
let height = 630

struct Copy {
    let title: String
    let summary: String
    let navBeforeTitle: String
    let navBeforeBody: String
    let navAfterTitle: String
    let navAfterBody: String
    let scheduleBeforeTitle: String
    let scheduleBeforeBody: String
    let scheduleAfterTitle: String
    let scheduleAfterBody: String
    let caveat: String
}

func color(_ hex: Int) -> NSColor {
    NSColor(
        calibratedRed: CGFloat((hex >> 16) & 255) / 255,
        green: CGFloat((hex >> 8) & 255) / 255,
        blue: CGFloat(hex & 255) / 255,
        alpha: 1
    )
}

func rect(_ x: CGFloat, _ top: CGFloat, _ w: CGFloat, _ h: CGFloat,
          fill: NSColor, radius: CGFloat = 0) {
    fill.setFill()
    let area = NSRect(x: x, y: CGFloat(height) - top - h, width: w, height: h)
    NSBezierPath(roundedRect: area, xRadius: radius, yRadius: radius).fill()
}

func draw(_ value: String, _ x: CGFloat, _ top: CGFloat, _ w: CGFloat,
          _ h: CGFloat, size: CGFloat, shade: NSColor,
          bold: Bool = false, alignment: NSTextAlignment = .left) {
    let font = NSFont.systemFont(ofSize: size, weight: bold ? .semibold : .regular)
    let paragraph = NSMutableParagraphStyle()
    paragraph.lineBreakMode = .byWordWrapping
    paragraph.alignment = alignment
    (value as NSString).draw(
        in: NSRect(x: x, y: CGFloat(height) - top - h, width: w, height: h),
        withAttributes: [
            .font: font,
            .foregroundColor: shade,
            .paragraphStyle: paragraph
        ]
    )
}

let isKorean = CommandLine.arguments.count > 1 && CommandLine.arguments[1] == "ko"
let root = CommandLine.arguments.count > 2 ? CommandLine.arguments[2] : "."
let copy: Copy

if isKorean {
    copy = Copy(
        title: "열지 않은 레시피가 요청을 만들었다",
        summary: "Spoonie PR #48, #49, #50 · 2026.11.19",
        navBeforeTitle: "입력 없이 RSC 사전 요청 10건",
        navBeforeBody: "touchstart에서도 미열람 레시피를 미리 요청",
        navAfterTitle: "회귀 테스트에서 유휴 요청 0건",
        navAfterBody: "마우스 hover·키보드 focus에서만 준비, 탭 이동 유지",
        scheduleBeforeTitle: "레시피 공개 1일 3회",
        scheduleBeforeBody: "구형 Instagram 재시도 1일 4회",
        scheduleAfterTitle: "두 예약 작업 제거",
        scheduleAfterBody: "기존 함수 주소는 HTTP 410 반환",
        caveat: "390×844 모바일 Chromium 회귀 테스트 · 월간 함수 사용량 변화는 미측정"
    )
} else {
    copy = Copy(
        title: "A recipe link prefetching before a tap",
        summary: "Spoonie PR #48, #49 and #50 · 2026.11.19",
        navBeforeTitle: "10 RSC prefetches with no input",
        navBeforeBody: "touchstart also warmed unopened recipe cards",
        navAfterTitle: "Zero idle prefetch in regression QA",
        navAfterBody: "Mouse hover or keyboard focus only; tap still navigates",
        scheduleBeforeTitle: "3 Recipe releases per day",
        scheduleBeforeBody: "4 legacy Instagram retries per day",
        scheduleAfterTitle: "Both schedules retired",
        scheduleAfterBody: "Former function URLs now return HTTP 410",
        caveat: "390×844 mobile Chromium regression · monthly function usage change not measured"
    )
}

guard let bitmap = NSBitmapImageRep(
    bitmapDataPlanes: nil,
    pixelsWide: width,
    pixelsHigh: height,
    bitsPerSample: 8,
    samplesPerPixel: 4,
    hasAlpha: true,
    isPlanar: false,
    colorSpaceName: .deviceRGB,
    bytesPerRow: 0,
    bitsPerPixel: 0
), let graphics = NSGraphicsContext(bitmapImageRep: bitmap) else {
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
let white = color(0xFFFFFF)

rect(0, 0, CGFloat(width), CGFloat(height), fill: paper)
rect(0, 0, CGFloat(width), 8, fill: teal)
draw("SPOONIE", 55, 35, 240, 34, size: 23, shade: ink, bold: true)
draw("ENGINEERING NOTE  /  2026.11.19", 690, 39, 455, 28,
     size: 16, shade: muted, alignment: .right)
draw(copy.title, 55, 94, 1090, 70,
     size: isKorean ? 46 : 45, shade: ink, bold: true)
draw(copy.summary, 58, 169, 1085, 36, size: 22, shade: muted)

rect(55, 225, 1090, 142, fill: white, radius: 16)
draw("NAVIGATION", 80, 244, 240, 24, size: 15, shade: teal, bold: true)
draw("BEFORE", 80, 274, 180, 23, size: 14, shade: muted, bold: true)
draw(copy.navBeforeTitle, 80, 299, 450, 30, size: 21, shade: ink, bold: true)
draw(copy.navBeforeBody, 80, 332, 450, 27, size: 17, shade: muted)
draw("→", 568, 294, 48, 42, size: 31, shade: teal, bold: true, alignment: .center)
draw("AFTER", 650, 274, 180, 23, size: 14, shade: muted, bold: true)
draw(copy.navAfterTitle, 650, 299, 445, 30, size: 21, shade: ink, bold: true)
draw(copy.navAfterBody, 650, 332, 445, 27, size: 17, shade: muted)

rect(55, 385, 1090, 142, fill: white, radius: 16)
draw("SCHEDULES", 80, 404, 240, 24, size: 15, shade: teal, bold: true)
draw("BEFORE", 80, 434, 180, 23, size: 14, shade: muted, bold: true)
draw(copy.scheduleBeforeTitle, 80, 459, 450, 30, size: 21, shade: ink, bold: true)
draw(copy.scheduleBeforeBody, 80, 492, 450, 27, size: 17, shade: muted)
draw("→", 568, 454, 48, 42, size: 31, shade: teal, bold: true, alignment: .center)
draw("AFTER", 650, 434, 180, 23, size: 14, shade: muted, bold: true)
draw(copy.scheduleAfterTitle, 650, 459, 445, 30, size: 21, shade: ink, bold: true)
draw(copy.scheduleAfterBody, 650, 492, 445, 27, size: 17, shade: muted)

rect(55, 550, 1090, 2, fill: border)
draw(copy.caveat, 58, 567, 1085, 30,
     size: isKorean ? 16 : 17, shade: muted)

NSGraphicsContext.restoreGraphicsState()

guard let data = bitmap.representation(using: .png, properties: [:]) else {
    fatalError("Unable to encode PNG")
}
let destination = URL(fileURLWithPath: root)
    .appendingPathComponent("assets/img/dev/spoonie-rsc-prefetch-20261119", isDirectory: true)
try FileManager.default.createDirectory(
    at: destination,
    withIntermediateDirectories: true
)
let filename = isKorean ? "spoonie-rsc-prefetch-ko.png" : "spoonie-rsc-prefetch-en.png"
let output = destination.appendingPathComponent(filename)
try data.write(to: output, options: .atomic)
print("\(output.path) \(data.count) bytes")
