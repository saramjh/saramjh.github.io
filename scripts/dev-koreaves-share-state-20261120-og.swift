import AppKit
import Foundation

let W = 1200, H = 630
let locale = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "en"
let root = CommandLine.arguments.count > 2 ? CommandLine.arguments[2] : "."
let ko = locale == "ko"
func color(_ c: Int) -> NSColor { NSColor(calibratedRed: CGFloat((c >> 16) & 255) / 255, green: CGFloat((c >> 8) & 255) / 255, blue: CGFloat(c & 255) / 255, alpha: 1) }
func box(_ x: CGFloat,_ top: CGFloat,_ w: CGFloat,_ h: CGFloat,_ fill: NSColor,_ radius: CGFloat = 0) {
    fill.setFill()
    NSBezierPath(roundedRect: NSRect(x: x, y: CGFloat(H) - top - h, width: w, height: h), xRadius: radius, yRadius: radius).fill()
}
func text(_ s: String,_ x: CGFloat,_ top: CGFloat,_ w: CGFloat,_ h: CGFloat,_ sz: CGFloat,_ ink: NSColor,_ bold: Bool = false) {
    let p = NSMutableParagraphStyle()
    p.lineBreakMode = .byWordWrapping
    (s as NSString).draw(in: NSRect(x: x, y: CGFloat(H) - top - h, width: w, height: h), withAttributes: [.font: NSFont.systemFont(ofSize: sz, weight: bold ? .semibold : .regular), .foregroundColor: ink, .paragraphStyle: p])
}
func stroke(_ x1: CGFloat,_ y1: CGFloat,_ x2: CGFloat,_ y2: CGFloat,_ ink: NSColor,_ w: CGFloat = 2) {
    let path = NSBezierPath()
    path.lineWidth = w
    path.move(to: NSPoint(x: x1,y: CGFloat(H) - y1))
    path.line(to: NSPoint(x: x2,y: CGFloat(H) - y2))
    ink.setStroke(); path.stroke()
}

guard let rep = NSBitmapImageRep(bitmapDataPlanes: nil,pixelsWide: W,pixelsHigh: H,bitsPerSample: 8,samplesPerPixel: 4,hasAlpha: true,isPlanar: false,colorSpaceName: .deviceRGB,bytesPerRow: 0,bitsPerPixel: 0),
      let context = NSGraphicsContext(bitmapImageRep: rep) else { fatalError("bitmap") }
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = context
context.imageInterpolation = .high
let bg = color(0xF6F5EF), ink = color(0x18342D), subtle = color(0x63766C), pine = color(0x24604A), rule = color(0xD7DDD4), white = color(0xFFFFFF)
box(0,0,1200,630,bg)
box(0,0,1200,8,pine)
text("KOREAVES / EVIDENCE ATLAS",58,31,550,29,20,ink,true)
text(ko ? "개발 구현  ·  2026.10.12" : "IMPLEMENTED  ·  OCTOBER 12, 2026",825,34,320,22,15,subtle)
text(ko ? "선택한 새를 다음 화면까지" : "Keep the selected bird",58,94,1090,67,46,ink,true)
text(ko ? "공유 링크에도 같은 종과 관련 조건을 남깁니다" : "Carry species and view context into the shared link",60,164,1080,43,25,subtle)
text(ko ? "복원 우선순위" : "SELECTION RESOLUTION",58,226,260,24,17,pine,true)
let labels = ko ? ["명시된 URL / 정식 종 경로", "현재 탭 선택", "마지막 방문 선택"] : ["Explicit URL / Species route", "Current tab selection", "Last-visit selection"]
let widths: [CGFloat] = [365,310,310]
let xs: [CGFloat] = [58,468,838]
for i in 0..<3 {
    box(xs[i],258,widths[i],66,white,12)
    box(xs[i],258,5,66,i==0 ? pine : color(0xB5C3B9),2)
    text(labels[i], xs[i]+20,274,widths[i]-30,36,ko ? 18 : 19,i==0 ? ink : subtle,i==0)
}
text("→",431,270,27,35,27,pine,true)
text("→",798,270,27,35,27,pine,true)
text(ko ? "종이 선택된 뒤 공유하는 화면" : "WHAT EACH SHARED VIEW PRESERVES",58,355,700,23,17,pine,true)
let rows: [(String,String,String)] = ko ? [
    ("GIS", "선택한 종 + 지정한 지역", "taxon · region"),
    ("SOURCES", "선택한 종 + 근거·출처 필터", "taxon · claim · source"),
    ("COMPARE", "중복 없는 비교 종 2~3개", "taxa = 2–3 IDs")
] : [
    ("GIS", "Selected bird + chosen region", "taxon · region"),
    ("SOURCES", "Bird + claim and source filters", "taxon · claim · source"),
    ("COMPARE", "Two or three distinct birds", "taxa = 2–3 IDs")
]
for i in 0..<3 {
    let y = CGFloat(389+i*56)
    if i % 2 == 0 { box(58,y,1085,51,color(0xEBF0E9),7) }
    text(rows[i].0,77,y+13,150,26,17,ink,true)
    text(rows[i].1,245,y+11,575,28,19,ink)
    text(rows[i].2,859,y+13,260,25,15,subtle)
    if i < 2 { stroke(58,y+53,1143,y+53,rule,1) }
}
stroke(58,571,1143,571,rule,2)
text(ko ? "브라우저 저장 상태는 공유 URL에 포함되지 않습니다." : "Browser memory and local UI state are not embedded in shared URLs.",58,581,1080,28,17,subtle)
NSGraphicsContext.restoreGraphicsState()
guard let raw = rep.representation(using: .png,properties: [:]) else { fatalError("encode") }
let bytes = [UInt8](raw), sig: [UInt8] = [137,80,78,71,13,10,26,10]
guard Array(bytes.prefix(8)) == sig else { fatalError("png") }
var output = Data(bytes.prefix(8)), offset = 8, ended = false
while offset + 12 <= bytes.count {
    let n = (UInt32(bytes[offset]) << 24) | (UInt32(bytes[offset+1]) << 16) | (UInt32(bytes[offset+2]) << 8) | UInt32(bytes[offset+3])
    let len = Int(n)
    guard len <= bytes.count - offset - 12 else { fatalError("chunk") }
    let type = String(bytes:bytes[(offset+4)..<(offset+8)],encoding:.ascii) ?? ""
    if !["eXIf", "tEXt", "iTXt"].contains(type) { output.append(contentsOf:bytes[offset..<(offset+len+12)]) }
    offset += len+12
    if type == "IEND" { ended = true; break }
}
guard ended && offset == bytes.count else { fatalError("png end") }
let path = URL(fileURLWithPath:root).appendingPathComponent("_posts/koreaves-selected-bird-share-links-\(ko ? "ko" : "en")/og.png")
try output.write(to:path,options:.atomic)
print("\(path.path): \(output.count) bytes")
