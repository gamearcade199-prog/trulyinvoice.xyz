// DEBUG: Check what invoice IDs look like
console.log('Sample invoice from your console errors:');
console.log('ID: f4f79498-cd...074b15');
console.log('ID: 2ee13a99-07...fcba1b2');
console.log('ID: 5dc616f8-7f...9c68cf2');

// These look like UUID format
// The issue might be that the [id] route is not matching these UUID patterns

export default function DebugPage() {
  return (
    <div className="p-8">
      <h1>DEBUG INVOICE IDS</h1>
      <p>Check the console for ID patterns</p>
    </div>
  )
}