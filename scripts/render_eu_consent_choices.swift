import AppKit
import Foundation

// First-party Jekyll footer flow, based on _includes/footer.html at d3ce5a1.
// This is an original code diagram. It does not depict any real visitor or consent UI.
let language = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "en"
guard ["ko", "en"].contains(language) else { fatalError("Expected en or ko") }
let destination = CommandLine.arguments.count > 2 ? CommandLine.arguments[2] :
  "assets/img/dev-eu-consent-choices-20261110/consent-choices-\(language).png"
let ko = language == "ko"
let w = 1200
let h = 630
guard let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil,
  pixelsWide: w, pixelsHigh: h, bitsPerSample: 8, samplesPerPixel: 4,
  hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB,
  bytesPerRow: 0, bitsPerPixel: 0),
  let graphics = NSGraphicsContext(bitmapImageRep: bitmap) else {
  fatalError("Unable to initialize original diagram")
}
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = graphics
let paper = NSColor(srgbRed: 0.967, green: 0.961, blue: 0.938, alpha: 1)
let ink = NSColor(srgbRed: 0.115, green: 0.171, blue: 0.191, alpha: 1)
let faded = NSColor(srgbRed: 0.370, green: 0.427, blue: 0.445, alpha: 1)
let divider = NSColor(srgbRed: 0.780, green: 0.791, blue: 0.775, alpha: 1)
let green = NSColor(srgbRed: 0.075, green: 0.455, blue: 0.391, alpha: 1)
let orange = NSColor(srgbRed: 0.650, green: 0.342, blue: 0.210, alpha: 1)
func fill(_ x: CGFloat, _ top: CGFloat, _ width: CGFloat, _ height: CGFloat, _ color: NSColor) {
  color.setFill()
  NSRect(x:x,y:CGFloat(h)-top-height,width:width,height:height).fill()
}
func stroke(_ x1: CGFloat, _ y1: CGFloat, _ x2: CGFloat, _ y2: CGFloat,
            color: NSColor, width: CGFloat = 2) {
  color.setStroke()
  let p=NSBezierPath()
  p.lineWidth=width
  p.move(to:NSPoint(x:x1,y:CGFloat(h)-y1))
  p.line(to:NSPoint(x:x2,y:CGFloat(h)-y2))
  p.stroke()
}
func label(_ text:String,_ x:CGFloat,_ top:CGFloat,_ size:CGFloat,_ color:NSColor,
           _ weight:NSFont.Weight = .regular,_ max:CGFloat = 1100) {
  let attrs:[NSAttributedString.Key:Any]=[
    .font:NSFont.systemFont(ofSize:size,weight:weight),
    .foregroundColor:color
  ]
  let measured=(text as NSString).size(withAttributes:attrs).width
  guard measured <= max else {fatalError("Text overflow \(language): \(text), \(measured) > \(max)")}
  (text as NSString).draw(at:NSPoint(x:x,y:CGFloat(h)-top-size*1.27),withAttributes:attrs)
}
fill(0,0,1200,630,paper)
fill(0,0,11,630,green)
label("DEVTESTUDINIDAE     /     JEKYLL PRIVACY ENGINEERING",66,40,21,green,.semibold,1065)
label(ko ? "동의 철회 링크의 표시 조건" : "When consent controls appear",66,91,51,ink,.bold,1085)
label(ko ? "원본 푸터 코드 기반 흐름도 · 실제 방문자 화면이 아님"
         : "A source-code schematic, not a real visitor session",66,159,24,faded,.regular,1070)
fill(66,226,1068,2,divider)

label(ko ? "광고 사용 블로그 글" : "AD-ENABLED POST",66,257,22,ink,.semibold,270)
label("page.ads != false",66,298,19,faded,.regular,260)
stroke(320,304,371,304,color:green,width:3)
label("›",361,276,42,green,.semibold,40)
label("CONSENT_API_READY",407,257,22,ink,.semibold,355)
label(ko ? "Google API 준비 이벤트" : "Google API readiness",407,298,19,faded,.regular,345)
stroke(763,304,805,304,color:green,width:3)
label("›",792,276,42,green,.semibold,40)
label("TCF: gdprApplies?",849,257,22,ink,.semibold,294)
label(ko ? "동의 규칙 적용 여부" : "Consent rule applicability",849,298,18,faded,.regular,288)

stroke(1003,337,1003,363,color:divider,width:2)
stroke(281,389,1011,389,color:divider,width:2)
fill(66,416,1068,2,divider)
label(ko ? "TRUE  ·  동의 철회 링크 표시" : "TRUE  ·  Reveal privacy choices",66,441,30,green,.semibold,1050)
label("link.hidden = false    →    showRevocationMessage()",66,488,24,ink,.regular,1065)
label(ko ? "FALSE 또는 API 실패  ·  링크는 숨김 유지"
         : "FALSE or API unavailable  ·  Leave the link hidden",66,542,21,orange,.medium,1070)
fill(66,585,1068,2,divider)
label(ko ? "근거: 2026-10-08 원본 커밋 d3ce5a1 · 모의 동작 테스트 6건"
         : "Evidence: original commit d3ce5a1 · 6 mocked runtime checks",
      66,595,16,faded,.regular,1070)
graphics.flushGraphics()
NSGraphicsContext.restoreGraphicsState()
guard let png=bitmap.representation(using:.png,properties:[:]) else {fatalError("PNG encode failed")}
let url=URL(fileURLWithPath:destination)
try FileManager.default.createDirectory(at:url.deletingLastPathComponent(),withIntermediateDirectories:true)
try png.write(to:url,options:.atomic)
print("original diagram \(language): \(w)x\(h) bytes=\(png.count) path=\(destination)")
