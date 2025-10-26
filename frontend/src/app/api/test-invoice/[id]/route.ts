export async function GET(request: Request, { params }: { params: { id: string } }) {
  return Response.json({
    status: 'ok',
    invoiceId: params.id,
    message: 'Dynamic route is working'
  })
}
