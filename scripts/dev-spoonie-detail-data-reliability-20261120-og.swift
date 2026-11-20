import AppKit
import Foundation

let width = 1200
let height = 630

struct Copy {
    let title: String
    let summary: String
    let row1Label: String
    let row1Before: String
    let row1After: String
    let row2Label: String
    let row2Before: String
    let row2After: String
    let row3Label: String
    let row3Before: String
    let row3After: String
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
        title: "레시피 상세 조회 오류를 구분한다",
        summary: "Spoonie PR #23 · 2026.11.11 병합",
        row1Label: "백그라운드 갱신",
        row1Before: "이미 읽은 상세 데이터 + 일시적 오류",
        row1After: "기존 상세 내용 유지",
        row2Label: "접근 상태",
        row2Before: "항목 없음 또는 접근 거부",
        row2After: "오래된 캐시 숨김",
        row3Label: "Recipe 필수 데이터",
        row3Before: "재료 또는 조리 단계 조회 실패",
        row3After: "조회 실패를 오류 상태로 표시",
        caveat: "회귀 테스트 10건 추가 · 운영 DB 장애 주입은 미실시"
    )
} else {
    copy = Copy(
        title: "How Spoonie handles failed detail reads",
        summary: "Spoonie PR #23 · merged 2026.11.11",
        row1Label: "BACKGROUND REFRESH",
        row1Before: "Loaded detail data + temporary error",
        row1After: "Keep the loaded item visible",
        row2Label: "ACCESS STATE",
        row2Before: "Not found or access denied",
        row2After: "Hide stale cached content",
        row3Label: "RECIPE DATA",
        row3Before: "Ingredients or instructions query fails",
        row3After: "Keep query failures in an error state",
        caveat: "10 regression cases added · no production DB fault injection"
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
let green = color(0x1C6651)

rect(0, 0, CGFloat(width), CGFloat(height), fill: paper)
rect(0, 0, CGFloat(width), 8, fill: teal)
draw("SPOONIE", 55, 32, 220, 30, size: 21, shade: ink, bold: true)
draw("ENGINEERING NOTE  /  2026.11.20", 690, 36, 455, 25,
     size: 15, shade: muted, alignment: .right)
draw(copy.title, 55, 88, 1090, 66,
     size: isKorean ? 43 : 42, shade: ink, bold: true)
draw(copy.summary, 58, 158, 1085, 34, size: 21, shade: muted)

func row(_ top: CGFloat, label: String, before: String, after: String) {
    rect(55, top, 1090, 94, fill: white, radius: 13)
    draw(label, 78, top + 13, 250, 22, size: 14, shade: teal, bold: true)
    draw(before, 78, top + 43, 440, 34, size: 18, shade: ink, bold: true)
    draw("→", 555, top + 32, 50, 40, size: 28, shade: teal, bold: true, alignment: .center)
    draw(after, 645, top + 27, 455, 42, size: 20, shade: green, bold: true)
}

row(211, label: copy.row1Label, before: copy.row1Before, after: copy.row1After)
row(322, label: copy.row2Label, before: copy.row2Before, after: copy.row2After)
row(433, label: copy.row3Label, before: copy.row3Before, after: copy.row3After)

rect(55, 550, 1090, 2, fill: border)
draw(copy.caveat, 58, 566, 1085, 28,
     size: isKorean ? 16 : 16, shade: muted)

NSGraphicsContext.restoreGraphicsState()

guard let data = bitmap.representation(using: .png, properties: [:]) else {
    fatalError("Unable to encode PNG")
}

func stripTransportMetadata(_ png: Data) -> Data {
    let bytes = [UInt8](png)
    let signature: [UInt8] = [137, 80, 78, 71, 13, 10, 26, 10]
    guard bytes.count >= 8, Array(bytes.prefix(8)) == signature else {
        fatalError("Invalid generated PNG")
    }
    var output = Data(bytes.prefix(8))
    var offset = 8
    var sawEnd = false
    while offset + 12 <= bytes.count {
        let length =
            (UInt32(bytes[offset]) << 24) |
            (UInt32(bytes[offset + 1]) << 16) |
            (UInt32(bytes[offset + 2]) << 8) |
            UInt32(bytes[offset + 3])
        let size = Int(length)
        guard size <= bytes.count - offset - 12 else {
            fatalError("Invalid generated PNG chunk")
        }
        let type = String(bytes: bytes[(offset + 4)..<(offset + 8)],
                          encoding: .ascii) ?? ""
        if !["eXIf", "tEXt", "iTXt"].contains(type) {
            output.append(contentsOf: bytes[offset..<(offset + size + 12)])
        }
        offset += size + 12
        if type == "IEND" {
            sawEnd = true
            break
        }
    }
    guard sawEnd, offset == bytes.count else {
        fatalError("PNG data after IEND")
    }
    return output
}

let locale = isKorean ? "ko" : "en"
let destination = URL(fileURLWithPath: root)
    .appendingPathComponent("_posts/spoonie-detail-data-reliability-\(locale)", isDirectory: true)
try FileManager.default.createDirectory(
    at: destination,
    withIntermediateDirectories: true
)
let output = destination.appendingPathComponent("og.png")
let cleanData = stripTransportMetadata(data)
try cleanData.write(to: output, options: .atomic)
print("\(output.path) \(cleanData.count) bytes")
